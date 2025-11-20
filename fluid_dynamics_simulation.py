"""
2D Fluid Dynamics Simulation using Spectral Method (FFT)

This script sets up initial conditions for a 2D fluid dynamics simulation
using the spectral method via Fast Fourier Transform (FFT).
"""

# 1. Imports
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy.fft as nf


# 2. Spectral Helper Functions
def spekdel2(spek, KX, KY):
    """
    Calculate the 2D Laplacian (∇²) of the spectral coefficient.
    Formula: -(KX² + KY²) * spek
    
    Ensures boundary handling by setting KX column 0 and KY row 0 to 0.0
    on a copy of K.
    """
    KX_copy = KX.copy()
    KY_copy = KY.copy()
    KX_copy[:, 0] = 0.0
    KY_copy[0, :] = 0.0
    return -(KX_copy**2 + KY_copy**2) * spek


def invspekdel2(spek, KX, KY):
    """
    Calculate the inverse Laplacian.
    Formula: -spek / (KX² + KY²)
    
    The [0, 0] element (DC component) is set to 0.0 to avoid division by zero.
    """
    KX_copy = KX.copy()
    KY_copy = KY.copy()
    K2 = KX_copy**2 + KY_copy**2
    K2[0, 0] = 1.0  # Temporary value to avoid division by zero
    result = -spek / K2
    result[0, 0] = 0.0  # Set DC component to zero
    return result


def uspek(spek, KX, KY):
    """
    Calculate the u (zonal wind) component from streamfunction spectral coefficient.
    Formula: -i * KY * spek
    
    Ensures KY row 0 is set to 0.0 on a copy.
    """
    KY_copy = KY.copy()
    KY_copy[0, :] = 0.0
    return -1j * KY_copy * spek


def vspek(spek, KX, KY):
    """
    Calculate the v (meridional wind) component from streamfunction spectral coefficient.
    Formula: i * KX * spek
    
    Ensures KX column 0 is set to 0.0 on a copy.
    """
    KX_copy = KX.copy()
    KX_copy[:, 0] = 0.0
    return 1j * KX_copy * spek


def trunc(spek, Nt):
    """
    Truncate spectral coefficients by setting values in the corner to zero.
    Specifically, set the elements [0:Nt, :-Nt] of a copy of spek to 0.0.
    """
    spek_copy = spek.copy()
    spek_copy[0:Nt, :-Nt] = 0.0
    return spek_copy


# 3. Domain Parameters
km = 1e+3
Lx = 10000*km
Ly = 10000*km
Npoints = 256
Ntrunc = 10
beta = 0.0
deltat = 900


# 4. Wavenumber Setup
# Create spatial arrays
x = np.linspace(-Lx, Lx, Npoints)
y = np.linspace(-Ly, Ly, Npoints)

# Create mesh grids
xp, yp = np.meshgrid(x, y)

# Calculate 1D wavenumbers using fftfreq
# Normalize by the side length and multiply by 2π
dx = (x[1] - x[0]) / Lx
dy = (y[1] - y[0]) / Ly
kx = nf.fftfreq(Npoints, d=dx) * 2 * np.pi
ky = nf.fftfreq(Npoints, d=dy) * 2 * np.pi

# Create 2D wavenumber grids for derivatives (kx[0]=ky[0]=0)
KX, KY = np.meshgrid(kx, ky)

# Create 2D wavenumber grids for inversions (kx[0]=ky[0]=1 before meshing)
kx_u = kx.copy()
ky_u = ky.copy()
kx_u[0] = 1.0
ky_u[0] = 1.0
KXu, KYu = np.meshgrid(kx_u, ky_u)


# 5. Initial Conditions
# Calculate initial vorticity field in physical space
vor0 = (np.exp(-((xp - 3000*km)/Lx)**2 - (yp/Ly)**2) / 0.05) * 1e-5 \
       - (np.exp(-((xp + 3000*km)/Lx)**2 - (yp/Ly)**2) / 0.05) * 1e-5

# Transform to spectral space
s_vor0 = nf.fft2(vor0)

# Calculate initial streamfunction
s_str0 = invspekdel2(s_vor0, KXu, KYu)


# 6. Final Field Calculation
# Calculate spectral coefficients for final state using KX, KY grids
s_u0 = uspek(s_str0, KX, KY)
s_v0 = vspek(s_str0, KX, KY)

# Transform all spectral fields back to grid space
g_vor0 = nf.ifft2(s_vor0).real
g_u0 = nf.ifft2(s_u0).real
g_v0 = nf.ifft2(s_v0).real
g_str0 = nf.ifft2(s_str0).real


# 7. Visualization
# Create first figure with 2x2 subplot layout
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot vorticity
im0 = axes[0, 0].contourf(g_vor0)
axes[0, 0].set_title('Vorticity')
plt.colorbar(im0, ax=axes[0, 0])

# Plot u component
im1 = axes[0, 1].contourf(g_u0)
axes[0, 1].set_title('U Component')
plt.colorbar(im1, ax=axes[0, 1])

# Plot v component
im2 = axes[1, 0].contourf(g_v0)
axes[1, 0].set_title('V Component')
plt.colorbar(im2, ax=axes[1, 0])

# Plot streamfunction
im3 = axes[1, 1].contourf(nf.ifft2(s_str0).real)
axes[1, 1].set_title('Streamfunction')
plt.colorbar(im3, ax=axes[1, 1])

plt.tight_layout()
plt.show()

# Create second figure with quiver plot
fig2, ax = plt.subplots(1, 1, figsize=(10, 8))
ax.quiver(g_u0[::8, ::8], g_v0[::8, ::8], angles="xy")
ax.set_title('Velocity Vectors')
ax.set_aspect('equal')
plt.show()
