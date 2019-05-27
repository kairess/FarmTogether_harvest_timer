import gzip, shutil, json

# For Mac
# ~/Library/Application Support/Steam/userdata/########/673950/remote/Farms
path = '../Farms/farm_0.data'
json_path = '../Farms/farm_0.uc'

with gzip.open(path, 'r') as f:
  json_data = json.load(f)

json_data['Money']['Tickets'] = "10000"

with open(json_path, 'w') as f_out:
  json.dump(json_data, f_out)

with open(json_path, 'rb') as f_in:
  with gzip.open(path, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
