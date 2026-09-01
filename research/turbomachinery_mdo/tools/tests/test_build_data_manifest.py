"""Standard-library tests for the provenance manifest utility."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "build_data_manifest.py"
SPEC = importlib.util.spec_from_file_location("build_data_manifest", MODULE_PATH)
assert SPEC and SPEC.loader
MANIFEST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MANIFEST)


def level5_header() -> bytes:
    text = b"MATLAB 5.0 MAT-file, Platform: test, Created by manifest test"
    return text.ljust(116, b" ") + (b"\x00" * 8) + b"\x00\x01" + b"IM"


class BuildDataManifestTests(unittest.TestCase):
    def test_classifies_hashes_and_sorts_without_semantic_inference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "input"
            nested = root / "nested"
            nested.mkdir(parents=True)
            mat_path = nested / "b.mat"
            mat_path.write_bytes(level5_header() + b"payload")
            npz_path = root / "a.npz"
            npz_path.write_bytes(b"not-a-real-npz-but-a-provenance-test")
            (root / "ignored.txt").write_text("ignore", encoding="utf-8")

            result = MANIFEST.build_manifest(root, "GE-E3", {".mat", ".npz"})

            self.assertEqual([entry["relative_path"] for entry in result["files"]], ["a.npz", "nested/b.mat"])
            mat_record = result["files"][1]
            self.assertEqual(mat_record["mat_container"]["container"], "MATLAB Level 5-style header")
            self.assertEqual(mat_record["mat_container"]["endian_indicator"], "IM")
            self.assertEqual(mat_record["sha256"], hashlib.sha256(mat_path.read_bytes()).hexdigest())
            self.assertIn("without inferring", result["semantic_policy"])
            self.assertEqual(result["warnings"], [])

    def test_detects_v73_hdf5_signature_after_matlab_user_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "v73.mat"
            user_block = b"MATLAB 7.3 MAT-file, Platform: test".ljust(512, b"\x00")
            path.write_bytes(user_block + MANIFEST.HDF5_MAGIC + b"payload")

            result = MANIFEST.mat_container_metadata(path)

            self.assertEqual(result["container"], "HDF5 (possible MATLAB v7.3)")
            self.assertEqual(result["hdf5_signature_offset_bytes"], 512)

    def test_empty_directory_records_warning_not_nonexistence_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = MANIFEST.build_manifest(Path(temporary), "Pak-B", {".mat"})

            self.assertEqual(result["files"], [])
            self.assertEqual(len(result["warnings"]), 1)
            self.assertIn("not evidence", result["warnings"][0])

    def test_atomic_json_output_is_valid_and_replaces_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "manifests" / "result.json"
            payload = {"z": [1], "a": "中文"}
            MANIFEST.atomic_write_json(output, payload)

            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), payload)
            self.assertFalse(any(output.parent.glob(".result.json.tmp-*")))


if __name__ == "__main__":
    unittest.main()
