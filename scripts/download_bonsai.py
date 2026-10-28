#!/usr/bin/env python3
"""Download the pinned Mip-NeRF 360 Bonsai files and verify size/SHA-256."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import time
from pathlib import Path, PurePosixPath
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data_manifest.json"
DATA_ROOT = ROOT / "data" / "bonsai"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def target_for(record: dict) -> Path:
    rel = PurePosixPath(record["path"])
    if rel.is_absolute() or ".." in rel.parts or rel.parts[0] != "bonsai":
        raise ValueError(f"unsafe manifest path: {record['path']}")
    return DATA_ROOT.joinpath(*rel.parts[1:])


def verify_one(record: dict, download: bool, endpoint: str) -> tuple[Path, bool]:
    target = target_for(record)
    expected_size = int(record["size"])
    expected_sha = record.get("lfs", {}).get("oid")
    if target.is_file() and target.stat().st_size == expected_size:
        if not expected_sha or digest(target) == expected_sha:
            return target, True
    if not download:
        raise FileNotFoundError(f"missing or invalid file: {target.relative_to(ROOT)}")

    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(target.name + ".part")
    url = (
        f"{endpoint}/datasets/{record['repo_id']}/resolve/"
        f"{record['revision']}/{quote(record['path'], safe='/')}?download=true"
    )
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            h = hashlib.sha256()
            with requests.get(url, stream=True, timeout=(25, 120)) as response:
                response.raise_for_status()
                with temp.open("wb") as out:
                    for chunk in response.iter_content(1024 * 1024):
                        if chunk:
                            out.write(chunk)
                            h.update(chunk)
            if temp.stat().st_size != expected_size:
                raise ValueError(f"size mismatch for {record['path']}")
            if expected_sha and h.hexdigest() != expected_sha:
                raise ValueError(f"SHA-256 mismatch for {record['path']}")
            temp.replace(target)
            return target, False
        except Exception as exc:
            last_error = exc
            temp.unlink(missing_ok=True)
            if attempt < 4:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed downloading {record['path']}: {last_error}") from last_error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    endpoint = os.environ.get("HF_ENDPOINT", "https://huggingface.co").rstrip("/")
    records = []
    for item in manifest["files"]:
        item = dict(item)
        item["repo_id"] = manifest["mirror_repo"]
        item["revision"] = manifest["revision"]
        records.append(item)

    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(verify_one, item, not args.verify_only, endpoint) for item in records]
        for future in concurrent.futures.as_completed(futures):
            path, _ = future.result()
            done += 1
            if done % 25 == 0 or done == len(records):
                print(f"verified {done}/{len(records)}: {path.name}", flush=True)

    actual_bytes = sum(target_for(item).stat().st_size for item in records)
    expected_bytes = int(manifest["bytes"])
    if len(records) != int(manifest["count"]) or actual_bytes != expected_bytes:
        raise SystemExit(f"manifest total mismatch: files={len(records)}, bytes={actual_bytes}")
    print(f"PASS: {len(records)} files, {actual_bytes} bytes; SHA-256 checked where available")


if __name__ == "__main__":
    main()
