import pygame, math, time, copy, random

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return 'v -> ' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z)

    def mul_mat4x4(self, mat):
        x = self.x * mat[0][0] + self.y * mat[1][0] + self.z * mat[2][0] + 1.0 * mat[3][0]
        y = self.x * mat[0][1] + self.y * mat[1][1] + self.z * mat[2][1] + 1.0 * mat[3][1]
        z = self.x * mat[0][2] + self.y * mat[1][2] + self.z * mat[2][2] + 1.0 * mat[3][2]
        w = self.x * mat[0][3] + self.y * mat[1][3] + self.z * mat[2][3] + 1.0 * mat[3][3]

        self.x = x
        self.y = y
        self.z = z

        if not w == 0:
            self.x = self.x / w
            self.y = self.y / w
            self.z = self.z / w

    def translate(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = [0,0,0]

    def __str__(self):
        return str(self.p1) + ' and ' + str(self.p2) + ' and ' + str(self.p3)

    def draw(self):
        p1x = (self.p1.x + 1.0) * screen_width / 2.0
        p1y = (self.p1.y + 1.0) * screen_height / 2.0
        p2x = (self.p2.x + 1.0) * screen_width / 2.0
        p2y = (self.p2.y + 1.0) * screen_height / 2.0
        p3x = (self.p3.x + 1.0) * screen_width / 2.0
        p3y = (self.p3.y + 1.0) * screen_height / 2.0
        pygame.draw.polygon(screen, self.color, [[int(p1x), int(p1y)], [int(p2x), int(p2y)], [int(p3x), int(p3y)]], 0)
        #pygame.draw.line(screen, [255,255,255], [int(p1x), int(p1y)], [int(p2x), int(p2y)], 2)
        #pygame.draw.line(screen, [255,255,255], [int(p2x), int(p2y)], [int(p3x), int(p3y)], 2)
        #pygame.draw.line(screen, [255,255,255], [int(p1x), int(p1y)], [int(p3x), int(p3y)], 2)

    def check_visibility(self):
        vector_to_camera = difference_vector(self.p1, camera_vec)
        line1 = difference_vector(self.p2, self.p1)
        line2 = difference_vector(self.p3, self.p1)
        normal_vector = cross_product(line1, line2)
        #print(str(self))
        #print(normal_vector)
        if dot_product(vector_to_camera, normal_vector) < 0:
            tris_to_draw.append(self)
            light_value = dot_product(normal_vector, light_dir)
            if light_value < 0:
                light_value = 0
            #light_value += 1.0
            #light_value /= 2.0
            #print('light_value is', light_value)
            self.color = [light_value * 255.0, light_value * 255.0, light_value * 255.0]

    def mul_mat4x4(self, mat):
        self.p1.mul_mat4x4(mat)
        self.p2.mul_mat4x4(mat)
        self.p3.mul_mat4x4(mat)

    def translate(self, x, y, z):
        self.p1.translate(x,y,z)
        self.p2.translate(x,y,z)
        self.p3.translate(x,y,z)

class Figure:
    def __init__(self, tris):
        self.tris = tris

    def draw(self):
        for tri in self.tris:
            tri.draw()

    def check_visibility(self):
        for tri in self.tris:
            tri.check_visibility()

    def mul_mat4x4(self, mat):
        for tri in self.tris:
            tri.mul_mat4x4(mat)

    def translate(self, x, y, z):
        for tri in self.tris:
            tri.translate(x, y, z)

def get_z_rot_mat(theta):
    rot_z_mat = [[0 for x in range(4)] for y in range(4)]
    rot_z_mat[0][0] = math.cos(theta)
    rot_z_mat[0][1] = math.sin(theta)
    rot_z_mat[1][0] = -math.sin(theta)
    rot_z_mat[1][1] = math.cos(theta)
    rot_z_mat[2][2] = 1
    return rot_z_mat

def get_x_rot_mat(theta):
    rot_x_mat = [[0 for x in range(4)] for y in range(4)]
    rot_x_mat[0][0] = 1
    rot_x_mat[1][1] = math.cos(theta)
    rot_x_mat[1][2] = math.sin(theta)
    rot_x_mat[2][1] = -math.sin(theta)
    rot_x_mat[2][2] = math.cos(theta)
    return rot_x_mat

def get_y_rot_mat(theta):
    rot_y_mat = [[0 for x in range(4)] for y in range(4)]
    rot_y_mat[0][0] = math.cos(theta)
    rot_y_mat[0][2] = -math.sin(theta)
    rot_y_mat[1][1] = 1
    rot_y_mat[2][0] = math.sin(theta)
    rot_y_mat[2][2] = math.cos(theta)
    return rot_y_mat

def sum_vector(a,b):
    sum_vector = Vector(0,0,0)
    sum_vector.x = a.x + b.x
    sum_vector.y = a.y + b.y
    sum_vector.z = a.z + b.z
    return sum_vector

def difference_vector(a,b):
    difference_vector = Vector(0,0,0)
    difference_vector.x = a.x - b.x
    difference_vector.y = a.y - b.y
    difference_vector.z = a.z - b.z
    return difference_vector

def dot_product(a,b):
    return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)

def cross_product(a,b):
    cross = Vector(0,0,0)
    cross.x = (a.y * b.z) - (a.z * b.y)
    cross.y = (a.z * b.x) - (a.x * b.z)
    cross.z = (a.x * b.y) - (a.y * b.x)
    norm_vector(cross)
    return cross

def norm_vector(v):
    l = math.sqrt(math.pow(v.x,2.0) + math.pow(v.y, 2.0) + math.pow(v.z, 2.0))
    if not l == 0:
        v.x /= l
        v.y /= l
        v.z /= l

def get_geo_from_file(file_loc):
    global average_z
    geo = []
    vecs = []

    file = open(file_loc, 'r')
    lines = file.readlines()

    for line in lines:
        parts = str.split(line)
        if parts[0] == 'v':
            vecs.append(Vector(float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == 'f':
            first_vector = copy.deepcopy(vecs[int(parts[1]) - 1])
            second_vector = copy.deepcopy(vecs[int(parts[2]) - 1])
            third_vector = copy.deepcopy(vecs[int(parts[3]) - 1])
            geo.append(Triangle(first_vector, second_vector, third_vector))

    sum_x = 0.0
    sum_y = 0.0
    sum_z = 0.0
    for vec in vecs:
        sum_x += vec.x
        sum_y += vec.y
        sum_z += vec.z
    average_x = sum_x / float(len(vecs))
    average_y = sum_y / float(len(vecs))
    average_z = sum_z / float(len(vecs))
    print('average x is', average_x)
    print('average y is', average_y)
    print('average z is', average_z)
    for g in geo:
        g.translate(-average_x, -average_y, -average_z)

    file.close()
    return geo


cube_tris = []
#south
cube_tris.append(Triangle(Vector(0,0,0), Vector(0,1,0), Vector(1,1,0)))
cube_tris.append(Triangle(Vector(1,1,0), Vector(1,0,0), Vector(0,0,0)))
#east
cube_tris.append(Triangle(Vector(1,0,0), Vector(1,1,0), Vector(1,1,1)))
cube_tris.append(Triangle(Vector(1,1,1), Vector(1,0,1), Vector(1,0,0)))
#north
cube_tris.append(Triangle(Vector(1,0,1), Vector(1,1,1), Vector(0,1,1)))
cube_tris.append(Triangle(Vector(0,1,1), Vector(0,0,1), Vector(1,0,1)))
#west
cube_tris.append(Triangle(Vector(0,0,1), Vector(0,1,1), Vector(0,1,0)))
cube_tris.append(Triangle(Vector(0,1,0), Vector(0,0,0), Vector(0,0,1)))
#top
cube_tris.append(Triangle(Vector(0,1,0), Vector(0,1,1), Vector(1,1,1)))
cube_tris.append(Triangle(Vector(1,1,1), Vector(1,1,0), Vector(0,1,0)))
#bottom
cube_tris.append(Triangle(Vector(0,0,0), Vector(1,0,0), Vector(1,0,1)))
cube_tris.append(Triangle(Vector(1,0,1), Vector(0,0,1), Vector(0,0,0)))

cube = Figure(cube_tris)

pumpkin = Figure(get_geo_from_file("C:\\Users\\joels\\Documents\\Programming Resources\\teddy.obj"))

screen_width = 600.0
screen_height = 600.0
viewing_angle = math.pi/2.0
z_near = 0.1
z_far = 1000.0
camera_vec = Vector(0,0,0)

light_dir = Vector(0,0,1)
norm_vector(light_dir)

aspect_ratio = screen_width / screen_height
zoom_scale = 1.0 / math.tan(viewing_angle / 2.0)
scale_to_z = z_far / (z_far - z_near)

projection_mat = [[0 for x in range(4)] for y in range(4)]
projection_mat[0][0] = aspect_ratio * zoom_scale
projection_mat[1][1] = zoom_scale
projection_mat[2][2] = scale_to_z
projection_mat[3][2] = -z_near * scale_to_z
projection_mat[2][3] = 1

pygame.init()
screen = pygame.display.set_mode([int(screen_width), int(screen_height)])

delta_time = 0.01
theta = 0

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    theta += math.pi / 6.0 * delta_time

    screen.fill([0,0,0])
    tris_to_draw = []

    x_rot_mat = get_x_rot_mat(theta)
    z_rot_mat = get_z_rot_mat(theta * 2.0)
    y_rot_mat = get_y_rot_mat(theta)

    display_pumpkin = copy.deepcopy(pumpkin)
    display_pumpkin.mul_mat4x4(x_rot_mat)
    display_pumpkin.mul_mat4x4(z_rot_mat)
    display_pumpkin.translate(0,1,average_z - 35)
    display_pumpkin.check_visibility()

    tris_to_draw.sort(key=lambda x: (x.p1.z + x.p2.z + x.p3.z), reverse=False)
    for tri in tris_to_draw:
        tri.mul_mat4x4(projection_mat)
        tri.draw()

    #display_cube = copy.deepcopy(cube)

    ##display_cube.mul_mat4x4(x_rot_mat)
    #display_cube.mul_mat4x4(z_rot_mat)
    #display_cube.mul_mat4x4(y_rot_mat)
    #display_cube.translate(0,0,4)
    #display_cube.check_visibility()

    #display_cube.mul_mat4x4(projection_mat)
    #display_cube.draw()

    pygame.display.flip()
    time.sleep(delta_time)

pygame.quit()
