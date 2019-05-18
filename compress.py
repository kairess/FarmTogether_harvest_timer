import gzip, shutil

# For Mac
# ~/Library/Application Support/Steam/userdata/########/673950/remote/Farms
path = '../Farms/farm_0.json'

with open(path, 'rb') as f_in:
  with gzip.open('../Farms/farm_0.data', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
