# CFD-DEM Simulation of Particle Clogging with Shape Effects

This repository contains the coupled PFC3D-OpenFOAM simulation framework used in the paper:

> **Particle shape and clogging in fluid-driven flow: A coupled CFD-DEM study**  
> Z. Qiu, Q. Xiao, H. Yuan, X. Han, C. Li  
> *Powder Technology*, 437 (2024) 119566  
> https://doi.org/10.1016/j.powtec.2024.119566

The OpenFOAM coupling infrastructure (pyDemFoam solver, p2p coupling) is based on:  
https://github.com/itascaconsulting/PFC3D_OpenFOAM

## Software Requirements

- **PFC 3D 7.0** (Itasca) — DEM solver for particle simulation
- **OpenFOAM v2112+** — CFD solver
- **pyDemFoam** — Custom Python-wrapped OpenFOAM solver with porosity and drag coupling (see upstream repository for build instructions)
- **Python 3** with `numpy` and `itasca` module


## Repository Structure

### OpenFOAM Case

| Path | Description |
|---|---|
| `0/U` | Velocity initial/boundary condition (inlet: 0.1 m/s fixedValue) |
| `0/p` | Pressure initial/boundary condition (outlet: 0 fixedValue) |
| `0/f` | Volumetric force field (DEM drag coupling, initialized to zero) |
| `0/n` | Porosity field (initialized to 1.0, updated during coupling) |
| `constant/transportProperties` | Fluid properties (ν = 1×10⁻⁶, ρ = 1000) |
| `constant/polyMesh/` | OpenFOAM mesh files |
| `system/blockMeshDict` | Mesh geometry definition (two-block domain) |
| `system/controlDict` | Solver control (icoFoam, endTime = 2, deltaT = 5×10⁻⁶) |
| `system/decomposeParDict` | Parallel decomposition (6 subdomains, 3×2×1) |
| `system/fvSchemes` | Numerical schemes (Euler, Gauss linear) |
| `system/fvSolution` | Solver settings (PISO, PCG, smoothSolver) |
| `system/refineMeshDict` | Mesh refinement configuration |
| `system/topoSetDict` | Cell zone selection |

### PFC DEM Scripts

| Path | Description |
|---|---|
| `PFCIni.py` | PFC initialization — creates mesh from CFD data, generates walls, saves `create_mesh.sav` |
| `PFCLOAD2.PY` | **Main coupling loop** — nested loop (40 × 200 steps, dt = 5×10⁻⁵), saves checkpoints at each outer step |
| `PFCload.py` | Alternative coupling loop (single loop, 2000 steps, dt = 2×10⁻⁴) — functionally similar to PFCLOAD2.PY |
| `gen_wall.dat` | Wall geometry definition |
| `gen_ball2.dat` | Spherical ball (sphere) particle generation |
| `gen_clump.dat` | Clump (non-spherical) particle generation |

### CFD Coupling Scripts

| Path | Description |
|---|---|
| `CFDIni.py` | CFD-side initialization — connects to PFC, sends mesh nodes/elements and fluid properties |
| `CFDload.py` | CFD-side main loop — receives porosity and drag from PFC, solves flow, sends back pressure and velocity |

### Project Files

| Path | Description |
|---|---|
| `sandF.prj` | PFC 3D project file (references saved states from various simulation stages) |
| `post.fis` | FISH functions for in-simulation monitoring (mass balance, CFD section velocity/pressure, contact tracking, porosity-based timestep adjustment) |

### Geometry Source (meshing reference)

| Path | Description |
|---|---|
| `mesh/xushanlin.igs` | CAD geometry (IGES format) |
| `mesh/Xushanlin.scdoc` | Ansys SpaceClaim geometry file |
| `mesh/xushanlin.wbpj` | Ansys Workbench project |

### Post-processing (optional)

| Path | Description |
|---|---|
| `post.py` | PFC Python post-processing — restores saved models, computes mean contact forces, exports bitmaps |
| `post info/` | Simulation output data (contact forces, particle counts, MATLAB scripts, history files, figures) |
| `ballnum.asv` | MATLAB script for ball number analysis |

## How to Run

1. **Generate OpenFOAM mesh:**
   ```
   blockMesh
   ```

2. **Initialize CFD-PFC coupling:**
   - Terminal 1 (CFD side): `python CFDIni.py`
   - Terminal 2 (PFC side): `pfc3d700_console call PFCIni.py`

3. **Run coupled simulation:**
   - Terminal 1: `python CFDload.py`
   - Terminal 2: `pfc3d700_console call PFCLOAD2.PY`

   The two scripts run simultaneously and communicate via TCP/IP (p2pLink). PFC sends porosity and drag forces to CFD; CFD returns pressure, pressure gradient, and velocity to PFC.

## Notes

- `PFCload.py` and `PFCLOAD2.PY` serve similar purposes with different loop structures. `PFCLOAD2.PY` uses a nested loop with periodic checkpoint saving and was the primary version used in the paper.
- The `pyDemFoam` solver (`pyDemIcoFoam`) is a modified version of OpenFOAM's `icoFoam` that includes porosity and body force terms for DEM coupling. Refer to the [upstream repository](https://github.com/itascaconsulting/PFC3D_OpenFOAM) for build and installation instructions.
- The simulation domain consists of two blocks: an inlet reservoir section (50 mm × 7.2 mm × 7.2 mm) and a main channel section (22 mm × 7.2 mm × 2.4 mm), representing a microfluidic constriction channel.

## Citation

If you use this code in your research, please cite:

```bibtex
@article{qiu2024particle,
  title = {Particle shape and clogging in fluid-driven flow: A coupled CFD-DEM study},
  author = {Qiu, Z. and Xiao, Q. and Yuan, H. and Han, X. and Li, C.},
  journal = {Powder Technology},
  volume = {437},
  pages = {119566},
  year = {2024},
  doi = {10.1016/j.powtec.2024.119566}
}
```


