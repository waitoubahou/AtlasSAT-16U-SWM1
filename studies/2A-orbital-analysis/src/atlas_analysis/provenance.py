"""Input fingerprints and fresh-run output isolation. No persistent result cache."""
import hashlib
import json
import platform
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()

def code_fingerprint(root):
    files = sorted((root/"src").rglob("*.py"))
    return hashlib.sha256("".join(p.relative_to(root).as_posix()+sha256(p) for p in files).encode()).hexdigest()

def fingerprint(root, oem, config_path, targets, config):
    files = [Path(oem).resolve(), Path(config_path).resolve(), Path(targets).resolve()]
    for rel, expected in config["geographic_integrity"].items():
        path = root/rel
        if sha256(path) != expected:
            raise ValueError(f"Geographic input changed: {rel}; review and explicitly revise its pin")
        files.append(path)
    for item in config["kernels"]:
        path = Path(item["path"])
        files.append(path if path.is_absolute() else root/path)
    hashes = {str(path): sha256(path) for path in files}
    result = dict(files=hashes, code_sha256=code_fingerprint(root), python=platform.python_version())
    result["fingerprint"] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    # Gate identity deliberately excludes selected targets: three -> full-ROI transfer.
    result["model_fingerprint"] = hashlib.sha256(
        (sha256(oem)+sha256(config_path)+result["code_sha256"]+
         json.dumps(config["geographic_integrity"], sort_keys=True)).encode()).hexdigest()
    return result

def new_run_directory(root, tag):
    if not tag or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in tag):
        raise ValueError("Run tag must contain only letters, digits, underscore or hyphen")
    directory = root/"analysis_runs"/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"_"+tag+"_"+uuid4().hex[:8])
    directory.mkdir(parents=True, exist_ok=False)
    return directory

def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")

