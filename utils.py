import os
import numpy as np
from collections import Counter

color_continuous_scale=[(0,'rgb(23, 23, 121)'), 
                        (0.25, 'rgb(0, 166, 80)'), 
                        (0.5,'rgb(216, 218, 120)'), 
                        (0.75,'rgb(98, 64, 57)'), 
                        (1,'rgb(255, 255, 255)')]
def get_color_scale(min_level, max_level, sealevel = 500):
    diff = max_level - min_level
    color_continuous_scale=[[0,'rgb(23, 23, 121)'], 
                            [sealevel / diff * 1/3, 'rgb(135, 206, 235)'], 
                            [sealevel / diff * 2/3, 'rgb(0, 166, 80)'], 
                            [sealevel / diff + 1/3*(1-sealevel / diff),'rgb(216, 218, 120)'], 
                            [sealevel / diff + 2/3*(1-sealevel / diff),'rgb(98, 64, 57)'], 
                            [1,'rgb(255, 255, 255)']]
    return color_continuous_scale
# Renormalizes the values of `x` to `bounds`
def normalize(x, bounds=(0, 1)):
    return np.interp(x, (x.min(), x.max()), bounds)

# Fourier-based power law noise with frequency bounds.
def fbm(shape, p, lower=-np.inf, upper=np.inf, seed = 0, bounds=(0, 1)):
    np.random.seed(seed)
    freqs = tuple(np.fft.fftfreq(n, d=1.0 / n) for n in shape)
    freq_radial = np.hypot(*np.meshgrid(*freqs))
    envelope = (np.power(freq_radial, p, where=freq_radial!=0) *
               (freq_radial > lower) * (freq_radial < upper))
    envelope[0][0] = 0.0
    phase_noise = np.exp(2j * np.pi * np.random.rand(*shape))
    return normalize(np.real(np.fft.ifft2(np.fft.fft2(phase_noise) * envelope)), bounds)

# Simple gradient by taking the diff of each cell's horizontal and vertical
# neighbors.
def simple_gradient(a):
    dx = 0.5 * (np.roll(a, 1, axis=0) - np.roll(a, -1, axis=0))
    dy = 0.5 * (np.roll(a, 1, axis=1) - np.roll(a, -1, axis=1))
    return 1j * dx + dy

# Peforms a gaussian blur of `a`.
def gaussian_blur(a, sigma=1.0):
    freqs = tuple(np.fft.fftfreq(n, d=1.0 / n) for n in a.shape)
    freq_radial = np.hypot(*np.meshgrid(*freqs))
    sigma2 = sigma**2
    g = lambda x: ((2 * np.pi * sigma2) ** -0.5) * np.exp(-0.5 * (x / sigma)**2)
    kernel = g(freq_radial)
    kernel /= kernel.sum()
    return np.fft.ifft2(np.fft.fft2(a) * np.fft.fft2(kernel)).real

# Returns each value of `a` with coordinates offset by `offset` (via complex 
# values). The values at the new coordiantes are the linear interpolation of
# neighboring values in `a`.
def sample(a, offset):
    def lerp(x, y, a): return (1.0 - a) * x + a * y
    shape = np.array(a.shape)
    delta = np.array((offset.real, offset.imag))
    coords = np.array(np.meshgrid(*map(range, shape))) - delta

    lower_coords = np.floor(coords).astype(int)
    upper_coords = lower_coords + 1
    coord_offsets = coords - lower_coords 
    lower_coords %= shape[:, np.newaxis, np.newaxis]
    upper_coords %= shape[:, np.newaxis, np.newaxis]

    result = lerp(lerp(a[lower_coords[1], lower_coords[0]],
                       a[lower_coords[1], upper_coords[0]],
                       coord_offsets[0]),
                  lerp(a[upper_coords[1], lower_coords[0]],
                       a[upper_coords[1], upper_coords[0]],
                       coord_offsets[0]),
                  coord_offsets[1])
    return result

# Takes each value of a and offsets them by delta. Treats each grid point like a unit square.
def displace(a, delta):
    fns = {-1: lambda x: -x,
           0: lambda x: 1 - np.abs(x),
           1: lambda x: x,}
    result = np.zeros_like(a)
    for dx in range(-1, 2):
        wx = np.maximum(fns[dx](delta.real), 0.0)
        for dy in range(-1, 2):
            wy = np.maximum(fns[dy](delta.imag), 0.0)
            result += np.roll(np.roll(wx * wy * a, dy, axis=0), dx, axis=1)
    return result

def remove_duplicates(x, y):
    seen = set()
    x_unique = []
    y_unique = []
    for i in range(len(x)):
        if x[i] not in seen:
            seen.add(x[i])
            x_unique.append(x[i])
            y_unique.append(y[i])
    return x_unique, y_unique

def get_image_path(img):
    # Create a directory and save the uploaded image.
    file_path = f"data/uploadedImages/{img.name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as img_file:
        img_file.write(img.getbuffer())
    return file_path


def find_duplicates_sorted(lst):
    counter = Counter(lst)
    duplicates = sorted([item for item, count in counter.items() if count > 1])
    return duplicates

def sigmoid(arr, steepness=10, midpoint=0.5):
    return 1 / (1 + np.exp(-steepness * (arr - midpoint)))

from matplotlib import pyplot
pyplot.plot(np.linspace(0, 1, 100), sigmoid(np.linspace(0,1,100),10, 0.3))
pyplot.show()