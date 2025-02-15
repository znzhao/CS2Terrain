import cv2
import numpy as np
import copy
import streamlit as st
import numpy as np
from scipy.interpolate import PchipInterpolator
from utils import normalize, fbm, simple_gradient, gaussian_blur, sample, displace, find_duplicates_sorted, sigmoid

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
    

def process_terrain(CHN, params, input_terrain, intpl_inputs, progressing_text, progressed_text):
    blank = np.ones(shape=(512, 512))*12.5/100*4000
    input_terrain = cv2.resize(input_terrain, (512, 512))
    intpl_func = PchipInterpolator(params['intpl_x'], params['intpl_y'])
    levels = find_duplicates_sorted(params['intpl_y'])
    print(levels)
    if not levels:
        levels = [(params['max_altitude'] + params['min_altitude'])/2]

    bounds = (params['min_altitude'], params['max_altitude'])
    noise_terrain = fbm(input_terrain.shape, -2.0, seed=params['seed'], 
                        bounds = bounds)
    if np.array_equal(input_terrain, blank):
        input_display = noise_terrain
        # apply the noise on the map
        terrain = noise_terrain
    else:
        input_display = input_terrain
        input_weight = input_display - 500
        input_weight = (input_weight>0) * input_weight / np.max(input_weight) + (input_weight<0) * input_weight / np.min(input_weight)
        input_weight = normalize(input_weight, (0, params['noise_weight']))
        # apply the noise on the map
        noise_factors = normalize(noise_terrain, bounds=(0, params['noise_weight']))
        terrain = (1-input_weight)*input_terrain + input_weight*noise_factors
        terrain = (input_terrain > 500) * (1-noise_factors) * (input_terrain - 500)
        terrain += (input_terrain < 500) * (1-noise_factors) * (input_terrain - 500) + 500
        avg_factors = sigmoid(params['noise_weight'], 1, 0.9)
        terrain = (1-avg_factors) * terrain + avg_factors * (params['noise_weight'] * (noise_terrain - 500) + 500)

    terrain = normalize(terrain, bounds)
    terrain = intpl_func(terrain)

    # get levels:
    target = copy.deepcopy(terrain)
    weight = (target > max(levels)) * (target - max(levels))/ (np.max(target) - max(levels)) 
    weight += (target < min(levels)) * (min(levels) - target) / (min(levels) - np.min(target)) 
    weight = sigmoid(weight, 10, 0.3)
    # erode the terrain
    if params['erosion_params']['erosion']:
        shift_bounds = (params['min_altitude'], params['max_altitude'])
        shift_terrain = erode(terrain, params['erosion_params'], shift_bounds, progressing_text, progressed_text)
        if max(levels) != max(target):
            mounts = np.select([target > max(levels)], [shift_terrain], np.nan)
            mounts = mounts - abs(np.nanmin(mounts))
            mounts = np.nan_to_num(mounts, nan = 0)
            mounts = normalize(mounts, (0, params['max_altitude'] - max(levels)))
        else:
            mounts = np.zeros_like(terrain)
        if min(levels) != min(target):
            seas = np.select([target < min(levels)], [shift_terrain], np.nan)
            seas = seas - abs(np.nanmax(seas))
            seas = np.nan_to_num(seas, nan = 0)
            seas = normalize(seas, (params['min_altitude'] - min(levels), 0))
        else:
            seas = np.zeros_like(terrain)
        shift_terrain = mounts + seas

        flats = target * (target <= max(levels)) * (target >= min(levels)) + min(levels)*(target < min(levels)) + max(levels)*(target > max(levels))

        terrain = shift_terrain * weight + flats
    
    terrain = cv2.resize(terrain, (4096, 4096), interpolation=cv2.INTER_AREA)
    return terrain, input_display
