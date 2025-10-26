# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 23:27:21 2025

@author: jproj
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
plt.rcParams['figure.max_open_warning'] = 100  # Set


class Ray:
    def __init__(self, position, direction):
        self.position = np.array(position, dtype=float)
        self.direction = self._normalize(np.array(direction, dtype=float))
        self.path = [self.position.copy()]  # store path for plotting
    def _normalize(self, v):
        return v / np.linalg.norm(v)
    def point_at(self, t):
        """Return a point along the ray at parameter t"""
        return self.position + t * self.direction

    def intersect(self, surface_func, t_bounds=(0, 100)):
        """
        Find intersection point by minimizing vertical distance between ray and surface.
        surface_func(x) returns z value of surface at x.
                """
        def vertical_diff(t):
            x, y = self.point_at(t)
            z = surface_func(x)
            return (y - z) ** 2  # squared vertical difference
        try:
            sol = minimize_scalar(vertical_diff, bounds=t_bounds, method='bounded')
            if not sol.success:
                raise RuntimeError("Minimization failed.")
            intersection = self.point_at(sol.x)
            self.position = intersection
            self.path.append(intersection.copy())
        except RuntimeError as e:
            print(f"Skipping ray: {e}")
            return  # Or pass, depending on your logic


    def refract(self, surface_func, n1, n2, h=1e-7):
        x = self.position[0]
        if -1.8 <= x <= 1.8:
            dz_dx = (surface_func(x + h) - surface_func(x - h)) / (2 * h)
            normal = np.array([-dz_dx, 1.0])
            n = self._normalize(normal)
            k1 = self._normalize(self.direction)
            cos_theta_i = -np.dot(n, k1)
            eta = n1 / n2
            sin2_theta_t = eta**2 * (1 - cos_theta_i**2)
            cos_theta_t = np.sqrt(1 - sin2_theta_t)
            k2 = eta * k1 + (eta * cos_theta_i - cos_theta_t) * n
            self.direction = self._normalize(k2)
            return "OK"
    def passThrough(self, surface_func):
        x = self.position[0]
        position_i.append(x)
    def passThrough_2(self, surface_func):
        x = self.position[0]
        position_r.append(x)
    def refract_2(self, surface_func, n1, n2, h=1e-7):
        x = self.position[0]
        if -1.8 <= x <= 1.8:
            dz_dx = (surface_func(x + h) - surface_func(x - h)) / (2 * h)
            normal = np.array([-dz_dx, 1.0])
            n = self._normalize(normal)
            k1 = self._normalize(self.direction)
            cos_theta_i = -np.dot(n, k1)
            eta = n1 / n2
            sin2_theta_t = eta ** 2 * (1 - cos_theta_i ** 2)
            cos_theta_t = np.sqrt(1 - sin2_theta_t)
            k2 = eta * k1 + (eta * cos_theta_i + cos_theta_t) * n
            self.direction = self._normalize(k2)
            return "OK"

    def reflect(self, mirror_func, h=1e-7):
        x = self.position[0]
        if -6.35 <= x <= 6.35:
          self.direction[1] = -self.direction[1]
        #x = self.position[0]  # Current x-coordinate of the position
        #k = self.direction  # Direction of the ray in a 2D/3D space

        # Slope of the surface (dz/dx) using finite differences
        #dz_dx = (mirror_func(x + h) - mirror_func(x - h)) / (2 * h)
        #normal = np.array([-dz_dx, 1.0])
        # Compute theta (angle between ray direction and normal)
        #theta = np.arccos(np.dot(k,normal))
        #Mrot = np.array([
         #[np.cos(theta), -np.sin(theta)],
         #[np.sin(theta),  np.cos(theta)]
        #])
        #k1 = np.dot(Mrot,k)
        #self.direction = k1
        return 'OK'
    def get_path(self):
        return np.array(self.path)
    


# ##############################################################
# Structual functions for defining optical elements.
# ##############################################################
def aspheric_sag(x, R, k, A_coeffs, flip = 'no', offs = 0):
    """
    Compute sag z(x) for a rotationally symmetric asphere (Thorlabs convention).
    x can be scalar or numpy array.
    """
    c = 1 / R
    x2 = x**2
    base = (c * x2) / (1 + np.sqrt(1 - (1 + k) * c**2 * x2))
    poly = sum(A * x**(2 * i) for i, A in enumerate(A_coeffs, start=2))
    if flip == 'flip':
        return - base - poly + offs
    else:
        return + base + poly + offs
    
def plot_asphere(R, k, A_coeffs, x, ax, flip = 'no', offs=0):
    z = aspheric_sag(x, R, k, A_coeffs, flip, offs)
    ax.plot(x, z, label="Aspheric surface", c = 'tab:blue')
    
def flat(x, z):
    return z*(x/x)

def plot_flat(x, z, ax, color = 'tab:blue'):
    zs = flat(x, z)
    ax.plot(x, zs, label="Flat surface", color = color)
    
def plane(x, z):
    return z*(x/x)

def plot_plane(x, z, ax, label, color='blue'):
    za = plane(x, z)
    ax.plot(x, za, label=label, color=color)



position_i = []
position_r = []
# Parameters for the asphere (example: c660TME-C lens)
R = -2.305500
k = -1.0180000
A_coeffs = [-4.965900e-3, -5.916600e-5, 2.273900e-6, 2.128900e-6]
x_range = np.linspace(-1.8, 1.8, 100)
spread = []
spread2 = []
Z = 20
f_p = 1.583
spread2 = []
z_range2 = np.linspace(3.0,3.3,60)
for z in z_range2:
    f1 = -2.5
    f2 = f1 - z
    a2 = f2 - 2.5
    m1 = f1 - f_p - 12.99
    f_p1 = -f_p + f1

    fig, ax = plt.subplots()


    # Plot optical system
    plot_plane(x_range, f_p1, ax, 'Mid Plane', color='purple')
    plot_asphere(R, k, A_coeffs, x_range, ax)
    plot_flat(x_range, f1, ax)
    plot_flat(x_range, f2, ax)
    plot_asphere(R, k, A_coeffs, x_range, ax, 'flip', a2)
    plot_flat(x_range, m1, ax, color='k')

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-15, 1)
    ax.set_title("Ray intersection and refraction on aspheric surface, lens spacing: {:.2f} mm".format(z))
    ax.legend()
    ax.grid(True)
    fig.canvas.draw()

    ray_paths_2 = []

    for i in range(100):
        ray = Ray(position=[np.linspace(-1.8, 1.8, 100)[i], 1], direction=[0, -100])

        ### Optical path before mirror ###
        ray.intersect(lambda x: aspheric_sag(x, R, k, A_coeffs), t_bounds=(0, 10))
        ray.refract(lambda x: aspheric_sag(x, R, k, A_coeffs), n1=1.0, n2=1.77)

        ray.intersect(lambda x: flat(x, f1), t_bounds=(0, 10))
        ray.refract(lambda x: flat(x, f1), n1=1.77, n2=1.0)

        ray.intersect(lambda x: flat(x, f1), t_bounds=(0, 10))
        ray.passThrough(lambda x: plane(x, za))

        ray.intersect(lambda x: flat(x, f2), t_bounds=(0, 10))
        ray.refract(lambda x: flat(x, f2), n1=1.0, n2=1.77)

        ray.intersect(lambda x: aspheric_sag(x, R, k, A_coeffs, 'flip', a2), t_bounds=(0, 10))
        ray.refract(lambda x: aspheric_sag(x, R, k, A_coeffs, 'flip', a2), n1=1.77, n2=1.0)

        ray.intersect(lambda x: flat(x, m1), t_bounds=(0, 10))
        path_before_mirror = ray.get_path().copy()

        ### Reflection ###
        ray.reflect(lambda x: flat(x, m1))

        ### After mirror ###
        ray.intersect(lambda x: aspheric_sag(x, R, k, A_coeffs, 'flip', a2), t_bounds=(0, 10))
        ray.refract_2(lambda x: aspheric_sag(x, R, k, A_coeffs, 'flip', a2), n1=1.0, n2=1.77)

        ray.intersect(lambda x: flat(x, f2), t_bounds=(0, 10))
        ray.refract_2(lambda x: flat(x, f2), n1=1.77, n2=1.0)

        ray.intersect(lambda x: flat(x, f_p1), t_bounds=(0, 10))

        ray.intersect(lambda x: flat(x, f1), t_bounds=(0, 10))
        ray.refract_2(lambda x: flat(x, f1), n1=1.0, n2=1.77)

        ray.intersect(lambda x: aspheric_sag(x, R, k, A_coeffs), t_bounds=(0, 10))
        ray.refract_2(lambda x: aspheric_sag(x, R, k, A_coeffs), n1=1.77, n2=1.0)



        # Save the full path
        path_full = ray.get_path()
        ray_paths_2.append(path_full)

    ### After loop of 100 rays ###
    ps_21 = np.asarray(ray_paths_2)
    #plt.plot(ps_21[:, 9:, 0].T, ps_21[:, 9:, 1].T, 'b-', alpha=0.6)
    plt.plot(ps_21[:, 5:, 0].T, ps_21[:, 5:, 1].T, 'b-', alpha=0.6)
    #plt.plot(ps_21[:, :6, 0].T, ps_21[:, :6, 1].T, 'r-', alpha=0.3)
    pos = 9
    ps_2 = abs(np.asarray(ray_paths_2)[:,pos,0])
    Inter = np.sum(np.ones(ps_2.shape[0])[ps_2 < 1.8])
    s = np.sum(ps_2[ps_2 < 1.8])
    out = s/Inter
    spread2.append(out)


# After the sweep
spread2 = np.array(spread2)
index = np.nanargmin(spread2)  # use nanargmin in case there are NaNs
f_p2 = z_range2[index]
print('fp: {}'.format(f_p))
print("Best z position:", f_p2)

plt.figure()
plt.plot(z_range2, spread2, marker='o')
plt.xlabel('z (mm)')
plt.ylabel('Spread')
plt.title('Spread vs z')
plt.grid(True)
plt.show()