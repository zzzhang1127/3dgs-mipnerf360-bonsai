#!/usr/bin/env python3
"""Compute PSNR/SSIM on held-out renders using GraphDeco metric helpers."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from PIL import Image
from torchvision.transforms.functional import to_tensor

parser = argparse.ArgumentParser()
parser.add_argument("--gs-dir", type=Path, required=True)
parser.add_argument("--model-dir", type=Path, required=True)
parser.add_argument("--iteration", type=int, default=30000)
args = parser.parse_args()

sys.path.insert(0, str(args.gs_dir))
from utils.image_utils import psnr
from utils.loss_utils import ssim

base = args.model_dir / "test" / f"ours_{args.iteration}"
render_dir, gt_dir = base / "renders", base / "gt"
if not render_dir.is_dir() or not gt_dir.is_dir():
    raise SystemExit(f"test renders not found under {base}")
names = sorted(p.name for p in render_dir.glob("*.png"))
if not names or names != sorted(p.name for p in gt_dir.glob("*.png")):
    raise SystemExit("render and ground-truth PNG sets differ or are empty")

rows = []
for name in names:
    with Image.open(render_dir / name) as im:
        render = to_tensor(im.convert("RGB")).unsqueeze(0)
    with Image.open(gt_dir / name) as im:
        gt = to_tensor(im.convert("RGB")).unsqueeze(0)
    rows.append({"name": name, "psnr_db": float(psnr(render, gt)), "ssim": float(ssim(render, gt))})

summary = {
    "count": len(rows),
    "mean_psnr_db": sum(r["psnr_db"] for r in rows) / len(rows),
    "mean_ssim": sum(r["ssim"] for r in rows) / len(rows),
    "per_render": rows,
    "source": "GraphDeco utils.image_utils.psnr and utils.loss_utils.ssim",
}
out = args.model_dir / "metrics_test.json"
out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: summary[k] for k in ("count", "mean_psnr_db", "mean_ssim")}, indent=2))
print(f"wrote {out}")
