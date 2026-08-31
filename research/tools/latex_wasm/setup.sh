#!/usr/bin/env bash
# Re-fetch the pdftex.js engine (npm registry) and patch it for headless Node use.
set -e
cd "$(dirname "$0")"
TMP=$(mktemp -d)
cd "$TMP"
npm init -y >/dev/null 2>&1
npm install pdftex.js >/dev/null 2>&1
cd -
mkdir -p vendor
cp "$TMP/node_modules/pdftex.js/pdftex-worker.js" vendor/
cp "$TMP/node_modules/pdftex.js/pdftex-worker.data" vendor/
cp "$TMP/node_modules/pdftex.js/pdftex-worker.js.mem" vendor/
rm -rf "$TMP"
# patch for Node: XHR->fs handled by driver; worker patches for file injection & PDF return
python3 - <<'PY'
p = "vendor/pdftex-worker.js"; s = open(p).read()
old = 'addEventListener("message",(function(event){var m=event.data;if(m.type==="start"){start(m.source,m.options)}}));'
new = ('addEventListener("message",(function(event){var m=event.data;if(m.type==="start"){'
       'if(m.extraFiles){m.extraFiles.forEach(function(f){var fp=f.path;if(fp[0]!=="/"){fp="/"+fp}'
       'var parts=fp.split("/");var fn=parts.pop();var dir=parts.join("/");'
       'if(!dir){dir="/"}if(dir!=="/"){try{FS.createPath("/",dir.slice(1),true,true)}catch(e){}}'
       'if(f.b64){var bytes=new Uint8Array(Buffer.from(f.b64,"base64"));FS.createDataFile(dir,fn,bytes,true,true)}else{FS.writeFile(fp,f.data)}});}'
       'start(m.source,m.options,m.readBack)}}));')
assert old in s, "patch point 1"
s = s.replace(old, new)
old2 = 'function start(source,options){'
assert old2 in s, "patch point 2"
s = s.replace(old2, 'function start(source,options,readBack){', 1)
old3 = ('uint8Array=FS.readFile("input.pdf");var blob=new Blob([uint8Array],{type:"application/pdf"});'
        'var url=URL.createObjectURL(blob);uint8Array=FS.readFile("input.log");'
        'var log=(new TextDecoder("utf-8")).decode(uint8Array);'
        'postMessage({type:"finish",value:{success:true,url:url,log:log}})}')
new3 = ('var pdfB64=null;try{uint8Array=FS.readFile("input.pdf");var pdfBin="";'
        'for(var pi=0;pi<uint8Array.length;pi+=65536){pdfBin+=String.fromCharCode.apply(null,uint8Array.subarray(pi,pi+65536))}'
        'pdfB64=btoa(pdfBin)}catch(e){}'
        'var log=null;try{uint8Array=FS.readFile("input.log");log=(new TextDecoder("utf-8")).decode(uint8Array)}catch(e){}'
        'var readBackFiles={};if(readBack){readBack.forEach(function(rp){try{var d=FS.readFile(rp);var b="";'
        'for(var ri=0;ri<d.length;ri+=65536){b+=String.fromCharCode.apply(null,d.subarray(ri,ri+65536))}'
        'readBackFiles[rp]=btoa(b)}catch(e2){readBackFiles[rp]=null}})}'
        'postMessage({type:"finish",value:{success:true,url:null,log:log,pdf:pdfB64,files:readBackFiles}})}')
assert old3 in s, "patch point 3"
s = s.replace(old3, new3)
open(p, "w").write(s)
old4 = 'filename=nodePath["normalize"](filename);var ret=nodeFS["readFileSync"](filename);'
new4 = ('filename=nodePath["normalize"](filename);'
        'if(!nodePath["isAbsolute"](filename)&&typeof __LATEX_WASM_VENDOR_DIR__!=="undefined"){'
        'filename=nodePath["join"](__LATEX_WASM_VENDOR_DIR__,filename)};'
        'var ret=nodeFS["readFileSync"](filename);')
assert old4 in s, "patch point 4"
s = s.replace(old4, new4)
old5 = 'if(ENVIRONMENT_IS_NODE){process["exit"](status)}else if(ENVIRONMENT_IS_SHELL&&typeof quit==="function"){quit(status)}'
new5 = 'if(false){}else if(ENVIRONMENT_IS_SHELL&&typeof quit==="function"){quit(status)}'
assert old5 in s, "patch point 5"
s = s.replace(old5, new5)
# Persist patches 4 and 5 as well. (Patches 1--3 were written above.)
open(p, "w").write(s)
print("vendor worker patched")
PY
echo "setup done"
