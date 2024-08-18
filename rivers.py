import cv2
import random
from utils import fbm
from scipy.stats import qmc
from scipy.spatial import Delaunay
import numpy as np
from scipy.interpolate import RegularGridInterpolator

def gen_river_tris(terrain, radius = 0.025, seed = 0):
    dim = terrain.shape[0]
    engine = qmc.PoissonDisk(d=2, radius=radius, seed=seed)
    nodes = (dim-1) * engine.fill_space()
    x = np.linspace(0, dim-1, dim)
    y = np.linspace(0, dim-1, dim)
    f = RegularGridInterpolator((x, y), terrain)
    tri = Delaunay(nodes)
    node_heights = [f(center)[0] for center in nodes]
    return nodes, tri, node_heights

def fractal_breaks(segment_coors, bound_pt_coors, magnitude = 0.5, seed = 0):
    random.seed(seed)
    mid_pt = find_intersection(segment_coors, bound_pt_coors)
    noise = random.uniform(-1, 1)
    new_pt = mid_pt + magnitude * (noise > 0) * abs(noise) * (bound_pt_coors[0] - mid_pt) + magnitude * (noise < 0)  * abs(noise) * (bound_pt_coors[1] - mid_pt)
    segment_0 = [segment_coors[0], new_pt]
    segment_1 = [new_pt, segment_coors[1]]
    bound_0 = [(segment_coors[0] + bound_pt_coors[0])/2, (segment_coors[0] + bound_pt_coors[1])/2]
    bound_1 = [(segment_coors[1] + bound_pt_coors[0])/2, (segment_coors[1] + bound_pt_coors[1])/2]
    return new_pt, segment_0, segment_1, bound_0, bound_1

def find_intersection(segment_coors, bound_pt_coors):
    # Extract the endpoints of the line segments
    x1, y1 = segment_coors[0]
    x2, y2 = segment_coors[1]
    x3, y3 = bound_pt_coors[0]
    x4, y4 = bound_pt_coors[1]
    # Calculate the slopes
    m1 = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else None
    m2 = (y4 - y3) / (x4 - x3) if (x4 - x3) != 0 else None
    # Calculate the intercepts
    b1 = y1 - m1 * x1 if m1 is not None else x1
    b2 = y3 - m2 * x3 if m2 is not None else x3
    # Check if one of the slopes is None (i.e., the line is vertical)
    if m1 is None:
        x = x1
        y = m2 * x + b2
    elif m2 is None:
        x = x3
        y = m1 * x + b1
    else:
        # Calculate the intersection point
        if m1 == m2:
            return None  # Parallel lines, no intersection
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    return np.array([x, y])

class RiverNode:
    def __init__(self, id, coor, height):
        self.id = id
        self.coor = coor
        self.height = height        
        self.upstream = []

    def add_upstream(self, upstream_node):
        self.upstream.append(upstream_node)

    def display(self, level=0):
        indent = " " * level * 4
        print(f"{indent}{self.id}:{self.height}")
        for upstream_node in self.upstream:
            upstream_node.display(level + 1)
    
    def get_length(self):
        if not self.upstream:  # If there are no upstream nodes
            return 0
        else:
            return 1 + max(upstream_node.get_length() for upstream_node in self.upstream)
    
    def compute_water(self):
        if not self.upstream:
            self.water = 1
        else:
            self.water = sum(upstream_node.compute_water() for upstream_node in self.upstream)
        return self.water
    
def build_edge(curr_node: RiverNode, tri, node_heights, frac = 7, magnitude = 0.9, seed = 0):
    # obtain the quadrilaterals
    river_paths = []
    for upstream_node in curr_node.upstream:
        segment_ids = [curr_node.id, upstream_node.id]
        condition_curr = (tri.simplices[:,0] == curr_node.id) | (tri.simplices[:,1] == curr_node.id) | (tri.simplices[:,2] == curr_node.id)
        condition_upstream = (tri.simplices[:,0] == upstream_node.id) | (tri.simplices[:,1] == upstream_node.id) | (tri.simplices[:,2] == upstream_node.id)
        bound_tris = tri.simplices[np.where(condition_curr & condition_upstream)]
        bound_pts = list(set(bound_tris.ravel()) - set(segment_ids))
        bound_pt_coors = []
        for bound_pt in bound_pts:
            bound_pt_coor = (tri.points[bound_pt] + tri.points[curr_node.id] + tri.points[upstream_node.id])/3
            bound_pt_coors.append(bound_pt_coor)
        
        # fractional break the lines into small pieces
        river_path = [curr_node.coor, upstream_node.coor]
        this_round_segment = [[curr_node.coor, upstream_node.coor]]
        this_round_bound = [bound_pt_coors]
        for iter in range(frac):
            next_round_segment = []
            next_round_bound = []
            for i, segment_coor, bound_pt_coor in zip(range(len(this_round_segment)), this_round_segment, this_round_bound):
                new_pt, segment_0, segment_1, bound_0, bound_1 = fractal_breaks(segment_coor, bound_pt_coor, magnitude=magnitude, seed=i+seed)
                river_path.insert(2*i + 1, new_pt)
                next_round_segment += [segment_0, segment_1]
                next_round_bound += [bound_0, bound_1]
            this_round_segment, this_round_bound = next_round_segment, next_round_bound
        river_paths.append(river_path)
    return river_paths

def find_estuary(target, tri, node_heights):
    init_tri_id = tri.find_simplex(np.array(target))
    init_pt_ids = tri.simplices[init_tri_id]
    init_pt_ids = sorted(init_pt_ids, key=lambda x: node_heights[x])
    estuary_id = init_pt_ids[0]
    estuary_node = RiverNode(estuary_id, tri.points[estuary_id], node_heights[estuary_id])
    return estuary_node

def find_upstream(node_id, tri, node_heights, source, queue_id, order_id, prob_bifur = 0.2, seed = 0):
    np.random.seed(seed)
    random.seed(seed)
    # find all the points that are connected to the current node
    condition = (tri.simplices[:,0] == node_id) | (tri.simplices[:,1] == node_id) | (tri.simplices[:,2] == node_id)
    connected_tris = tri.simplices[np.where(condition)]
    connected_pt_ids = list(set(connected_tris.ravel()) - set([node_id]) - set(queue_id) - set(order_id))
    # find all of the points that are higher than the current node
    higher_pt_ids = [id for id in connected_pt_ids if node_heights[id] >= node_heights[node_id]]
    output_pt_ids = []

    if higher_pt_ids != []:
        candidate_ids = sorted(higher_pt_ids, key=lambda x: node_heights[x])
    else:
        candidate_ids = connected_pt_ids

    if len(candidate_ids) == 0:
        return output_pt_ids

    if np.random.rand() < prob_bifur and len(candidate_ids) > 1:
        n_upstream = random.choice(range(1, len(candidate_ids)))
    else:
        n_upstream = 1

    if np.random.rand() < prob_bifur:
        output_pt_ids = random.sample(candidate_ids, k = n_upstream)
    else:
        candidate_ids = sorted(candidate_ids, key=lambda x: np.linalg.norm(tri.points[x] - source))
        output_pt_ids = [candidate_ids[0]]

    return output_pt_ids

def build_river(source_coor, estuary_coor, tri, node_heights, prob_bifur = 0.2, max_length = 20, seed = 0):
    estuary = find_estuary(estuary_coor, tri, node_heights)
    queue, order = [estuary],[]
    queue_id, order_id = [estuary.id],[]

    source = np.array(source_coor)

    while (queue != []) and (estuary.get_length() < max_length):
        curr_node = queue.pop()
        curr_node_id = queue_id.pop()
        order.append(curr_node)
        order_id.append(curr_node_id)
        upstream_ids = find_upstream(curr_node.id, tri, node_heights, source, queue_id, order_id, prob_bifur, seed)
        print('This run: ', upstream_ids)
        print('queue: ', queue_id)
        if upstream_ids == []:
            continue
        for upstream_id in upstream_ids:
            if upstream_id not in queue_id and upstream_id not in order_id:
                upstream_node = RiverNode(upstream_id, tri.points[upstream_id], node_heights[upstream_id])
                curr_node.add_upstream(upstream_node)
                queue.append(upstream_node)
                queue_id.append(upstream_id)
    return estuary

def build_river_network(estuary, tri, node_heights, frac = 7, magnitude = 0.9, seed = 0):
    edges = []
    water_levels = []
    queue, order = [estuary],[]
    while queue != []:
        curr_node = queue.pop()
        new_edges = build_edge(curr_node, tri, node_heights, frac, magnitude, seed)
        edges += new_edges
        water_levels += [curr_node.water]*len(new_edges)
        order.append(curr_node)
        for upstream in curr_node.upstream:
            if upstream not in queue and upstream not in order:
                queue.append(upstream)
    return edges, water_levels

def point_to_line_segment_distance(x1, y1, x2, y2):
    x = np.arange(512)
    y = np.arange(512)
    xx, yy = np.meshgrid(x, y)
    line_vec = np.array([x2 - x1, y2 - y1])
    line_len = np.linalg.norm(line_vec)
    p_vec = np.stack((xx - x1, yy - y1), axis=-1)
    proj = np.sum(p_vec * line_vec, axis=-1) / line_len**2
    proj = np.clip(proj, 0, 1)
    proj_point = np.stack((x1 + proj * line_vec[0], y1 + proj * line_vec[1]), axis=-1)
    dist = np.linalg.norm(p_vec - proj_point, axis=-1)
    return dist

def point_to_line_segment_distance(x1, y1, x2, y2, dim):
    x = np.arange(dim)
    y = np.arange(dim)
    xx, yy = np.meshgrid(x, y)
    line_vec = np.array([x2 - x1, y2 - y1])
    line_len = np.linalg.norm(line_vec)
    p_vec = np.stack((xx - x1, yy - y1), axis=-1)
    xy_vec = np.stack((xx, yy), axis=-1)
    proj = np.sum(p_vec * line_vec, axis=-1) / line_len**2
    proj_clipped = np.clip(proj, 0, 1)
    proj_point = np.stack((x1 + proj_clipped * line_vec[0], y1 + proj_clipped * line_vec[1]), axis=-1)
    dist = np.linalg.norm(xy_vec - proj_point, axis=-1)
    return dist

def kernel_func(x, k = 0.1):
    return 1/(1+k*x)

def dist_to_river(edges, water_levels, river_width = 1, dim = 512, ):
    distances = np.ones((dim, dim)) * dim*dim
    for edge, water_level in zip(edges, water_levels):
        for river_node_id in range(len(edge)-1):
            x1, y1 = edge[river_node_id][0], edge[river_node_id][1]
            x2, y2 = edge[river_node_id+1][0], edge[river_node_id+1][1]
            dist_to_seg = point_to_line_segment_distance(x1, y1, x2, y2, dim)
            within_river_path = dist_to_seg < river_width * np.sqrt(water_level)
            distances = np.minimum(distances, within_river_path * dist_to_seg + (1-within_river_path)*np.ones((dim, dim)) * dim*dim)
    return distances

def gen_river_terrain(distances, river_depth = 20, kernel_func = kernel_func):
    return river_depth * kernel_func(distances)

def add_rivers_to_terrain(terrain, params, river_params):
    small_terrain = cv2.resize(terrain, (1024, 1024), interpolation=cv2.INTER_AREA)
    nodes, tri, node_heights = gen_river_tris(small_terrain, radius = river_params['radius'], seed = params['seed'])
    river_terrains = np.zeros((4096, 4096))
    for river_seed, source_x, source_y, estuary_x, estuary_y, \
        river_length, prob_bifur, frac, magnitude, river_width, river_depths in zip(river_params['river_seeds'], 
                                                                                    river_params['source_xs'], 
                                                                                    river_params['source_ys'], 
                                                                                    river_params['estuary_xs'], 
                                                                                    river_params['estuary_ys'], 
                                                                                    river_params['river_lengths'], 
                                                                                    river_params['prob_bifurs'], 
                                                                                    river_params['fracs'],
                                                                                    river_params['magnitudes'],
                                                                                    river_params['river_widths'],
                                                                                    river_params['river_depths'],
                                                                                    ):
        estuary = build_river((source_x, source_y), (estuary_x, estuary_y), tri, node_heights, prob_bifur, river_length, river_seed)
        estuary.compute_water()
        estuary.display()
        edges, water_levels = build_river_network(estuary, tri, node_heights, frac, magnitude, river_seed)
        distances = dist_to_river(edges, water_levels, river_width = river_width, dim = 1024)
        river_terrain = gen_river_terrain(distances, river_depth = river_depths, kernel_func = kernel_func)
        river_terrain = cv2.resize(river_terrain, (4096, 4096), interpolation=cv2.INTER_AREA)
        river_terrains += river_terrain
    return river_terrains