# Tested environment

| Component | Tested version |
|---|---|
| OS | Ubuntu Linux |
| Python | 3.12.13 |
| NVIDIA toolkit/driver | CUDA 12.4 |
| PyTorch | 2.4.0+cu118 |
| torchvision | 0.19.0+cu118 |
| NumPy | 1.26.4 |
| SciPy | 1.17.1 |
| OpenCV | 4.13.0.92 |
| Pillow | 12.2.0 |
| plyfile | 1.0.3 |
| tqdm | 4.67.3 |
| imageio / imageio-ffmpeg | 2.37.3 / 0.6.0 |
| ninja | 1.13.0 |

The CUDA extensions were built from the pinned GraphDeco submodules for `diff-gaussian-rasterization` and `simple-knn`. Fused-SSIM was not required for this run. The viewer is a prebuilt static export and does not need Node.js at runtime.

## Setup notes

- `requirements.txt` pins the tested CUDA 11.8 PyTorch wheels and Python packages.
- A working CUDA toolkit with `nvcc`, a C++ compiler, and Ninja are needed to build the CUDA extensions.
- `scripts/setup_environment.sh` clones GraphDeco at the tested commit, initializes only the two required CUDA submodules, and builds them into the active virtual environment.
- The original upstream environment file targets an older Python/PyTorch stack. This repository documents the newer stack actually used for the run.
- H20 memory and timing figures are measurements, not guarantees for other GPUs.
