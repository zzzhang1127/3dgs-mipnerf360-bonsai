# Attribution and third-party terms

## Dataset

The scene is **Bonsai** from Mip-NeRF 360.

- Official project page and downloads: https://jonbarron.info/mipnerf360/
- Paper: Jonathan T. Barron et al., “Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields,” CVPR 2022.
- Reproducible mirror: https://huggingface.co/datasets/YuanhaoXD/Mip-NeRF360/tree/df31214ab1a3d72e0e4bfa1bfb3c03132b5cbe22
- The mirror page labels its repository Apache-2.0. The official project page links to the original files but does not state a separate dataset license. Raw images and COLMAP files are not redistributed here; review source terms before other uses.

## 3D Gaussian Splatting

The unmodified GraphDeco reference repository is pinned at commit `54c035f7834b564019656c3e3fcc3646292f727d`:

- https://github.com/graphdeco-inria/gaussian-splatting
- The complete upstream license is copied to [LICENSES/GRAPHDECO-LICENSE.md](LICENSES/GRAPHDECO-LICENSE.md). It permits research/evaluation use and requires redistributed work and resulting derivatives to remain under its terms. Commercial use requires prior explicit permission.
- Citation: Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis, “3D Gaussian Splatting for Real-Time Radiance Field Rendering,” ACM TOG 42(4), 2023.

## Interactive viewer

The standalone viewer was generated with `@playcanvas/supersplat-viewer` 1.41.0. It is the existing official PlayCanvas viewer, not a custom app written for this experiment. Its MIT license and bundled dependency notices are included in the viewer bundle and `LICENSES/`.

## Project-authored files

The scripts and documentation written for this repository are MIT licensed under [LICENSE](LICENSE). Third-party components and the trained model remain governed by their own terms.
