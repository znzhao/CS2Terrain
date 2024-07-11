import cv2
import numpy as np
import scipy as sp
import streamlit as st
import numpy as np
from utils import normalize, fbm, simple_gradient, gaussian_blur, sample, displace

def apply_slippage(terrain, repose_slope, cell_width):
    delta = simple_gradient(terrain) / cell_width
    smoothed = gaussian_blur(terrain, sigma=1.5)
    should_smooth = np.abs(delta) > repose_slope
    result = np.select([should_smooth], [smoothed], terrain)
    return result

def erode(terrain, erosion_params, bounds, progressing_text, progressed_text):
    rain_rate = erosion_params['rain_rate']
    evaporation_rate = erosion_params['evaporation_rate']
    min_height_delta = erosion_params['min_height_delta']
    repose_slope = erosion_params['repose_slope']
    gravity = erosion_params['gravity']
    sediment_capacity_constant = erosion_params['sediment_capacity']
    dissolving_rate = erosion_params['dissolving_rate']
    deposition_rate = erosion_params['deposition_rate']
    terrain = normalize(terrain)
    full_width = 537
    dim = terrain.shape[0]
    shape = [dim] * 2
    cell_width = full_width / dim
    cell_area = cell_width ** 2
    rain_rate = rain_rate * cell_area
    # The numer of iterations is proportional to the grid dimension. 
    # This is to allow changes on one side of the grid to affect the other side.
    iterations = int(1.4 * dim)
    # Sediment is the amount of suspended dirt in the water. 
    # Terrain will be transfered to/from sediment depending on a number of different factors.
    sediment = np.zeros_like(terrain)
    # The amount of water. Responsible for carrying sediment.
    water = np.zeros_like(terrain)

    # The water velocity.
    velocity = np.zeros_like(terrain)
    progress_bar = st.progress(0, text=progressing_text)
    for i in range(0, iterations):
        water += np.random.rand(*shape) * rain_rate
        # Compute the normalized gradient of the terrain height to determine where water and sediment will be moving.
        gradient = np.zeros_like(terrain, dtype='complex')
        gradient = simple_gradient(terrain)
        gradient = np.select([np.abs(gradient) < 1e-10],
                             [np.exp(2j * np.pi * np.random.rand(*shape))],
                             gradient)
        gradient /= np.abs(gradient)
        
        # Compute the difference between teh current height the height offset by gradient.
        neighbor_height = sample(terrain, -gradient)
        height_delta = terrain - neighbor_height
        
        # The sediment capacity represents how much sediment can be suspended in
        # water. If the sediment exceeds the quantity, then it is deposited,
        # otherwise terrain is eroded.
        sediment_capacity = ((np.maximum(height_delta, min_height_delta) / cell_width) * velocity * water * sediment_capacity_constant)
        deposited_sediment = np.select(
            [height_delta < 0, sediment > sediment_capacity,],
            [np.minimum(height_delta, sediment), deposition_rate * (sediment - sediment_capacity),],
            # If sediment <= sediment_capacity
            dissolving_rate * (sediment - sediment_capacity))

        # Don't erode more sediment than the current terrain height.
        deposited_sediment = np.maximum(-height_delta, deposited_sediment)
        # Update terrain and sediment quantities.
        sediment -= deposited_sediment
        terrain += deposited_sediment
        sediment = displace(sediment, gradient)
        water = displace(water, gradient)

        # Smooth out steep slopes.
        terrain = apply_slippage(terrain, repose_slope, cell_width)
        # Update velocity
        velocity = gravity * height_delta / cell_width
        # Apply evaporation
        water *= 1 - evaporation_rate
        progress_bar.progress(i/iterations, text=progressing_text)

    progress_bar.progress(100, text=progressed_text)
    return normalize(terrain, bounds=bounds)
    

def process_terrain(CHN, params, input_terrain, progressing_text, progressed_text):
    input_terrain = cv2.resize(input_terrain, (512, 512))
    bounds = (params['min_altitude'], params['max_altitude'])
    noise_terrain = fbm(input_terrain.shape, -2.0, seed=params['seed'], 
                        bounds = bounds)
    # apply the noise on the map
    terrain = (1-params['noise_weight'])*input_terrain + params['noise_weight']*noise_terrain
    terrain = normalize(terrain, bounds)
    # erode the terrain
    if params['erosion_params']['erosion']:
        terrain = erode(terrain, params['erosion_params'], bounds, progressing_text, progressed_text)
    terrain = cv2.resize(terrain, (4096, 4096), interpolation=cv2.INTER_AREA)
    return terrain
