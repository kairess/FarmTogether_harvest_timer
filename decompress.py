import gzip, shutil

# For Mac
# ~/Library/Application Support/Steam/userdata/########/673950/remote/Farms
path = '../Farms/farm_0.data'

with gzip.open(path, 'r') as f_in, open('../Farms/farm_0.json', 'wb') as f_out:
  shutil.copyfileobj(f_in, f_out)
