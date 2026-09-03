#!/usr/bin/env python3
"""Build a provenance-only manifest for locally available GE-E3/Pak-B files.

This utility deliberately does not infer scientific semantics from file names,
MAT variable names, dimensions, or an upstream README.  It is intended to make
an actual data delivery auditable before any split, training, uncertainty, or
optimization result is reported.

The script has no required third-party dependency.  If SciPy or h5py is
available, it adds a best-effort MAT variable inventory; failure to import or
parse either library is recorded in the manifest rather than silently ignored.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CHUNK_BYTES = 1024 * 1024
HDF5_MAGIC = b"\x89HDF\r\n\x1a\n"


def sha256_file(path: Path) -> str:
    """Return a streaming SHA-256 digest without loading a dataset into RAM."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def mat_container_metadata(path: Path) -> dict[str, Any]:
    """Classify a MAT-like container from bytes only, without parsing variables."""
    try:
        with path.open("rb") as handle:
            # MATLAB v7.3 commonly puts an HDF5 signature after a 512-byte user block,
            # rather than at byte zero. Read enough to distinguish that case without
            # attempting to load scientific variables.
            head = handle.read(1024)
    except OSError as exc:
        return {"container": "unreadable", "error": f"{type(exc).__name__}: {exc}"}

    hdf5_offset = head.find(HDF5_MAGIC)
    if hdf5_offset >= 0:
        return {
            "container": "HDF5 (possible MATLAB v7.3)",
            "hdf5_signature_offset_bytes": hdf5_offset,
        }

    result: dict[str, Any] = {"container": "unclassified"}
    text_header = head[:116].decode("ascii", errors="replace").rstrip("\x00 ")
    if text_header:
        result["header_text"] = text_header
    if len(head) >= 128 and b"MATLAB" in head[:116]:
        result["container"] = "MATLAB Level 5-style header"
        result["version_bytes_hex"] = head[124:126].hex()
        result["endian_indicator"] = head[126:128].decode("ascii", errors="replace")
    return result


def optional_variable_inventory(path: Path, container: str) -> dict[str, Any]:
    """Return a non-semantic variable inventory when a compatible parser exists."""
    if path.suffix.lower() != ".mat":
        return {"status": "not_applicable"}

    if container.startswith("HDF5"):
        try:
            import h5py  # type: ignore[import-not-found]
        except ImportError:
            return {
                "status": "not_attempted",
                "reason": "h5py is not installed; install it only in a recorded environment",
            }
        try:
            variables: list[dict[str, Any]] = []
            with h5py.File(path, "r") as handle:
                def visitor(name: str, obj: Any) -> None:
                    if isinstance(obj, h5py.Dataset):
                        variables.append(
                            {
                                "path": name,
                                "shape": list(obj.shape),
                                "dtype": str(obj.dtype),
                            }
                        )

                handle.visititems(visitor)
            return {"status": "ok", "parser": "h5py", "variables": variables}
        except Exception as exc:  # Parser diagnostics belong in provenance output.
            return {"status": "parse_failed", "parser": "h5py", "error": f"{type(exc).__name__}: {exc}"}

    try:
        from scipy.io import whosmat  # type: ignore[import-not-found]
    except ImportError:
        return {
            "status": "not_attempted",
            "reason": "SciPy is not installed; install it only in a recorded environment",
        }
    try:
        variables = [
            {"name": name, "shape": list(shape), "matlab_class": matlab_class}
            for name, shape, matlab_class in whosmat(path)
        ]
        return {"status": "ok", "parser": "scipy.io.whosmat", "variables": variables}
    except Exception as exc:  # Supports compressed/corrupt/unsupported MAT diagnostics.
        return {"status": "parse_failed", "parser": "scipy.io.whosmat", "error": f"{type(exc).__name__}: {exc}"}


def iter_files(root: Path, suffixes: set[str]) -> Iterable[Path]:
    """Yield regular files in stable relative-path order."""
    selected = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in suffixes
    ]
    return sorted(selected, key=lambda path: path.relative_to(root).as_posix())


def build_file_record(root: Path, path: Path) -> dict[str, Any]:
    """Collect file-level provenance only; no split or physical-field inference."""
    stat = path.stat()
    record: dict[str, Any] = {
        "relative_path": path.relative_to(root).as_posix(),
        "bytes": stat.st_size,
        "sha256": sha256_file(path),
    }
    if path.suffix.lower() == ".mat":
        mat_info = mat_container_metadata(path)
        record["mat_container"] = mat_info
        record["variable_inventory"] = optional_variable_inventory(path, mat_info["container"])
    return record


def parse_suffixes(raw_suffixes: list[str]) -> set[str]:
    suffixes: set[str] = set()
    for raw in raw_suffixes:
        suffix = raw if raw.startswith(".") else f".{raw}"
        suffixes.add(suffix.lower())
    return suffixes


def build_manifest(root: Path, dataset_label: str, suffixes: set[str]) -> dict[str, Any]:
    """Build a deterministic, provenance-oriented manifest dictionary."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"--root is not a readable directory: {root}")

    files = [build_file_record(root, path) for path in iter_files(root, suffixes)]
    warnings: list[str] = []
    if not files:
        warnings.append("No matching files found. This is not evidence that a public dataset does not exist.")

    return {
        "manifest_schema": "turbomachinery-data-provenance/v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "dataset_label_user_supplied": dataset_label,
        "root_path_user_supplied": str(root),
        "included_suffixes": sorted(suffixes),
        "semantic_policy": (
            "File names, variable names, dimensions, and bytes are recorded without inferring "
            "sample counts, train/test assignments, physical units, field meanings, or shared case IDs."
        ),
        "files": files,
        "warnings": warnings,
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON atomically to avoid a half-written provenance record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    temporary.replace(path)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Directory containing locally obtained data files.")
    parser.add_argument("--dataset-label", required=True, help="Literal label supplied by the operator, e.g. GE-E3 or Pak-B.")
    parser.add_argument("--output", required=True, type=Path, help="Manifest JSON path to create or replace.")
    parser.add_argument(
        "--suffix",
        action="append",
        default=[".mat", ".npz"],
        help="Suffix to include; repeatable. Defaults to .mat and .npz.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        manifest = build_manifest(args.root, args.dataset_label, parse_suffixes(args.suffix))
        atomic_write_json(args.output, manifest)
    except (OSError, ValueError) as exc:
        print(f"manifest build failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    print(
        f"Wrote {args.output} with {len(manifest['files'])} file record(s). "
        "No scientific semantics or split assignments were inferred."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
