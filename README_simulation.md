# 2D Fluid Dynamics Simulation

This repository contains a complete Python script for setting up initial conditions for a 2D fluid dynamics simulation using the spectral method (Fast Fourier Transform).

## Script: `fluid_dynamics_simulation.py`

### Description
A self-contained Python script that implements a 2D fluid dynamics simulation using spectral methods. The script calculates initial vorticity fields, transforms them to spectral space, and computes velocity components and streamfunction.

### Requirements
- Python 3.x
- numpy
- matplotlib

### Installation
```bash
pip install numpy matplotlib
```

### Usage
```bash
python fluid_dynamics_simulation.py
```

The script will:
1. Set up the computational domain (10,000 km × 10,000 km with 256 grid points)
2. Calculate initial vorticity field with two counter-rotating vortices
3. Transform to spectral space using FFT
4. Compute streamfunction and velocity components
5. Display two figures:
   - **Figure 1**: 2×2 subplot showing contour plots of vorticity, U component, V component, and streamfunction
   - **Figure 2**: Quiver plot showing velocity vectors

### Key Features

#### Spectral Helper Functions
- `spekdel2()`: Calculates 2D Laplacian in spectral space
- `invspekdel2()`: Calculates inverse Laplacian
- `uspek()`: Computes zonal wind component from streamfunction
- `vspek()`: Computes meridional wind component from streamfunction
- `trunc()`: Truncates spectral coefficients

#### Domain Parameters
- Domain size: 10,000 km × 10,000 km
- Grid points: 256 × 256
- Spectral truncation: 10 wavenumbers
- Time step: 900 seconds

#### Physical Interpretation
The simulation creates two counter-rotating vortices positioned at ±3000 km from the domain center, demonstrating:
- Vorticity generation and evolution
- Streamfunction patterns
- Velocity field structure
- Spectral transformations

### Output
The script generates:
1. A 2×2 contour plot figure showing:
   - Vorticity field
   - U (zonal) wind component
   - V (meridional) wind component
   - Streamfunction
   
2. A quiver plot showing velocity vectors (downsampled every 8 grid points for clarity)

### Notes
- All boundary conditions are properly handled in spectral space
- The [0,0] spectral component (DC/average) is set to zero to avoid division by zero
- Wavenumber grids are normalized appropriately for FFT operations
- The script uses `nf.fftfreq()` for correct wavenumber spacing

## Author
Created for the mahdilogist.github.io portfolio repository.
