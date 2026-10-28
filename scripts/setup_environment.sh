#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"
UPSTREAM_COMMIT="54c035f7834b564019656c3e3fcc3646292f727d"
GS_DIR="$ROOT/third_party/gaussian-splatting"

command -v "$PYTHON_BIN" >/dev/null || { echo "Python 3.12 is required (override PYTHON_BIN if needed)." >&2; exit 2; }
command -v nvcc >/dev/null || { echo "CUDA nvcc is required to build the 3DGS extensions." >&2; exit 2; }
command -v git >/dev/null
"$PYTHON_BIN" -m venv "$ROOT/.venv"
source "$ROOT/.venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$ROOT/requirements.txt"

if [[ ! -d "$GS_DIR/.git" ]]; then
  mkdir -p "$ROOT/third_party"
  git clone https://github.com/graphdeco-inria/gaussian-splatting.git "$GS_DIR"
fi
git -C "$GS_DIR" fetch origin "$UPSTREAM_COMMIT"
git -C "$GS_DIR" checkout --detach "$UPSTREAM_COMMIT"
git -C "$GS_DIR" submodule update --init submodules/diff-gaussian-rasterization submodules/simple-knn
python -m pip install "$GS_DIR/submodules/diff-gaussian-rasterization"
python -m pip install "$GS_DIR/submodules/simple-knn"
echo "Environment ready. Activate with: source $ROOT/.venv/bin/activate"
