from map import map

# game settings
RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
MAP_WIDTH = len(map)
MAP_HEIGHT = len(map[0])
MAP_SIZE = max(MAP_WIDTH, MAP_HEIGHT)
ENEMIES = 10
FPS = 144

# ray casting settings
VERT_NUM_RAYS = WIDTH // 3
HOR_NUM_RAYS = HEIGHT // 6
FOV = VERT_NUM_RAYS / 60
DELTA_ANGLE = FOV / VERT_NUM_RAYS
TEXTURE_RES = 1024