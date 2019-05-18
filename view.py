import cv2
import numpy as np
import gzip, shutil, json, time

REFRESH_TIME = 5

# n of chunks
MAP_WIDTH = 5
MAP_HEIGHT = 5
# n of tiles
CHUNK_WIDTH = 40
CHUNK_HEIGHT = 20

TILE_LENGTH = 4

TILE_COLORS = {
  'empty': (0, 255, 0),
  'no_crop': (0, 85, 160),
  'harvest': (0, 0, 255)
}

path = '../Farms/farm_0.data'

while True:

  try:
    read_t = time.time()
    with gzip.open(path, 'r') as f:
      json_data = json.load(f)
  except:
    print('cannot open file!')

  canvas = np.zeros((MAP_HEIGHT*CHUNK_HEIGHT*TILE_LENGTH, MAP_WIDTH*CHUNK_WIDTH*TILE_LENGTH, 3), dtype=np.uint8)

  chunks = json_data['Chunks']

  for chunk in chunks:
    chunk_position = np.array(chunk['ChunkPosition'].split(','), np.int)
    chunk_unlocked = True if chunk['Unlocked'] == 'true' else False

    if not chunk_unlocked:
      continue

    # if not np.array_equal(chunk_position, [2, 4]):
    #   continue

    for tile in chunk['Tiles']:
      tile_position = np.array(tile['tile'].split(','), np.int)
      tile_state = int(tile['state'])
      # 0: empty(available)
      # 1: Crop(contents key exists) or 갈은땅(contents key not exists)
      # 2: 갈지않은밭, 3: Tree, 4: Animal, 5: ?, 6: Flower

      cv_position = chunk_position * [CHUNK_WIDTH, CHUNK_HEIGHT] + tile_position
      cv_position[1] = MAP_HEIGHT * CHUNK_HEIGHT - cv_position[1]

      if tile_state == 0:
        temp_canvas = canvas.copy()
        cv2.rectangle(temp_canvas, pt1=tuple(cv_position * TILE_LENGTH), pt2=tuple((cv_position + 1) * TILE_LENGTH - 1), color=(0, 255, 0), thickness=-1, lineType=cv2.LINE_AA)
        alpha = 0.2
        cv2.addWeighted(temp_canvas, alpha, canvas, 1 - alpha, 0, canvas)

      elif (tile_state == 1 and 'contents' not in tile) or tile_state == 2:
        cv2.rectangle(canvas, pt1=tuple(cv_position * TILE_LENGTH), pt2=tuple((cv_position + 1) * TILE_LENGTH - 1), color=(0, 85, 160), thickness=-1, lineType=cv2.LINE_AA)

      if 'contents' in tile:
        contents = tile['contents']

        if 'state' in contents:
          contents_id = contents['id']
          contents_state = int(contents['state'])

          # crop, tree, animal and flower
          if (tile_state == 1 and contents_state == 1) or (tile_state == 3 and contents_state == 0) or (tile_state == 4 and contents_state == 1) or (tile_state == 6 and contents_state == 1):
            cv2.rectangle(canvas, pt1=tuple(cv_position * TILE_LENGTH), pt2=tuple((cv_position + 1) * TILE_LENGTH - 1), color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)

  cv2.imshow('Farm Together Timer', canvas)
  if cv2.waitKey(REFRESH_TIME * 1000) == ord('q'):
    break
