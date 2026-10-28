"""Rebuild public publication derivatives only; no GMAT, GIS or access computation."""
from pathlib import Path
import argparse,shutil,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/"studies/2A-orbital-analysis"
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--tectonic",required=True);p.add_argument("--destination",type=Path,required=True);p.add_argument("--font-directory",type=Path)
a=p.parse_args();out=a.destination.resolve()
if out.exists():raise ValueError("Choose a new build destination")
if out.is_relative_to(STUDY/"documents") or "outputs" in [x.lower() for x in out.parts]:raise ValueError("Protected/source build destination")
out.mkdir(parents=True)
for name in ("documents","figures","evidence","third_party"):
 shutil.copytree(STUDY/name,out/name)
if a.font_directory:
 for f in a.font_directory.rglob("*.pfb"):shutil.copyfile(f,out/"documents"/f.name)
results=[]
for tex in sorted((out/"documents").glob("*_Public_RC_v0_2.tex")):
 proc=subprocess.run([a.tectonic,"--untrusted","--keep-logs","--keep-intermediates",tex.name],cwd=tex.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/(tex.stem+".console.txt")).write_bytes(proc.stdout)
 results.append(dict(source=tex.name,exit_code=proc.returncode))
 print(tex.name,proc.returncode,flush=True)
 if proc.returncode:
  print(proc.stdout.decode("utf-8",errors="replace")[-3000:],flush=True);break
(out/"BUILD_RESULTS.json").write_text(json.dumps(results,indent=2))
raise SystemExit(any(x["exit_code"] for x in results))
