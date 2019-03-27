import numpy as np
import requests
import subprocess
import csv
import json

#Import tile urls
urlfp = 'randolph_tile_urls.csv'
urlfile = open(urlfp)
raw_urls = list(csv.reader(urlfile))[0:]
urls = [item for sublist in raw_urls for item in sublist]

boundaries = list()
#Download the file
for i in range(4):
  print(i)
  tile = requests.get(urls[i], allow_redirects=True)
  filename = urls[i].rsplit('/', 1)[1]
  outfile = open(filename, 'wb')
  outfile.write(tile.content)
  outfile.close()

  #Get the extent
  raster_info = subprocess.check_output('gdalinfo -json ' + filename, shell=True)
  info = json.loads(raster_info.decode('utf8'))
  boundary = info["wgs84Extent"]["coordinates"][0]

  boundaries.append([urls[i], boundary])

#Write the urls out
with open('randolph_boundaries', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(boundaries)
csvfile.close()


print(boundaries)
print(boundaries[1])
