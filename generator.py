import cv2
from scipy.interpolate import PchipInterpolator
import simulation
import sys
import util
def fade(t):
    "6t^5 - 15t^4 + 10t^3, t between 0 and 1"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def fadeintpl(curr_height, intplx, loudness):
    def pos(arr, x):
        count = 0
        for num in arr:
            if num < x: count += 1
        return int(count)
    upper = pos(intplx, curr_height)
    lower = upper - 1
    t = fade((curr_height - intplx[lower]) / (intplx[upper] - intplx[lower]))
    scaler = loudness[lower] + t*(loudness[upper] - loudness[lower])
    return scaler

def processTerrain(sorted_intplx, sorted_loudness, dim, seed, ksize, init_size, noise_size, erosion, full_width, rain_rate, 
                   evaporation_rate, min_height_delta, repose_slope, gravity, min_altitude, max_altitude, input_height = None, 
                   progress_text = None, progress_text2 = None):
    input_height = cv2.blur(input_height, ksize)
    fadeintplvec = PchipInterpolator(sorted_intplx, sorted_loudness)
    shape = [dim] * 2
    details = util.fbm(shape, -2.0, seed=seed)

    # apply the noise on the map
    terrain = init_size*input_height + noise_size*details
    terrain = fadeintplvec(terrain)
    # rain erode
    if erosion:
        terrain = simulation.main(sys.argv, 
                                  full_width = full_width, 
                                  dim = dim, 
                                  rain_rate = rain_rate, 
                                  evaporation_rate = evaporation_rate,
                                  min_height_delta = min_height_delta,
                                  repose_slope = repose_slope,
                                  gravity = gravity,
                                  terrain = util.normalize(terrain),
                                  progress_text = progress_text,
                                  progress_text2 = progress_text2)
    terrain = util.normalize(terrain, bounds = (min_altitude/4000, max_altitude/4000))
    terrain = fadeintplvec(terrain)
    return terrain
