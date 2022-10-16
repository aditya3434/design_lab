import numpy as np

O = np.array([0., 0.35, -1.])  # Camera
Q = np.array([0., 0., 0.])  # Camera pointing direction

def normalize(x):
    x /= np.linalg.norm(x)
    return x

# Returns distance from O in direction of ray OD to plane P with normal vector N
def intersect_plane(O, D, P, N):
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d

# Returns distance from O in direction of ray OD to sphere with centre S and radius R
def intersect_sphere(O, D, S, R):
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf

def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])

def trace_ray(L, color_light, material, rayO, rayD, scene):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i
    
    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return
        
    # Find the object.
    obj = scene[obj_idx]

    # Point of intersection on the object.
    M = rayO + rayD * t

    # Properties of the object.
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    
    toL = normalize(L - M)
    toO = normalize(O - M)

    # Shadow: find if the point is shadowed or not.
    l = [intersect(M + N * .0001, toL, obj_sh) 
            for k, obj_sh in enumerate(scene) if k != obj_idx]

    if l and min(l) < np.inf:
        return
    
    # Color computation
    col_ray = material[0]
    col_ray += obj.get('diffuse_c', material[1]) * max(np.dot(N, toL), 0) * color
    col_ray += obj.get('specular_c', material[2]) * max(np.dot(N, normalize(toL + toO)), 0) ** material[3] * color_light

    return obj, M, N, col_ray

def add_sphere(position, radius, color):
    return dict(type='sphere', position=np.array(position), 
        radius=np.array(radius), color=np.array(color), reflection=.5)
    
def add_plane(position, normal):
    color_plane0 = 1. * np.ones(3)
    color_plane1 = 0. * np.ones(3)

    return dict(type='plane', position=np.array(position), 
        normal=np.array(normal),
        color=lambda M: (color_plane0 
            if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else color_plane1),
        diffuse_c=.75, specular_c=.5, reflection=.25)

def ray_tracer(data):

    width = 400
    height = 300

    max_reflections = 5
    img = np.zeros((height, width, 3))

    scene = []

    for obj in data['objects']:
        scene.append(add_sphere(obj[0], obj[1], obj[2]))

    scene.append(add_plane([0., -.5, 0.], [0., 1., 0.]))

    r = float(width) / height
    
    # Main loop
    for i, x in enumerate(np.linspace(-1, 1, width)):
        for j, y in enumerate(np.linspace(-1.0/r + 0.25, 1.0/r + 0.25, height)):
            col = np.zeros(3)
            Q[:2] = (x, y)
            D = normalize(Q - O)
            reflection_no = 0
            rayO, rayD = O, D
            reflection = 1.
            # Loop through initial and secondary rays.
            while reflection_no < max_reflections:
                traced = trace_ray(data["l_pos"], np.array(data["l_color"]), np.array(data["material"]), rayO, rayD, scene)
                if not traced:
                    break

                obj, M, N, col_ray = traced

                # Creating reflected ray

                rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
                reflection_no += 1
                col += reflection * col_ray
                reflection *= obj.get('reflection', 1.)

            img[height - j - 1, i, :] = np.clip(col, 0, 1)

    img *= 255
    img = img.astype(np.uint8)
    return img