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
i = 1
#Download the file
for url in urls:
  print(i)
  i = i + 1

  tile = requests.get(url, allow_redirects=True)
  filename = url.rsplit('/', 1)[1]
  outfile = open(filename, 'wb')
  outfile.write(tile.content)
  outfile.close()

  #Get the extent
  raster_info = subprocess.check_output('gdalinfo -json ' + filename, shell=True)
  info = json.loads(raster_info.decode('utf8'))
  boundary = info["wgs84Extent"]["coordinates"][0]

  boundaries.append([url, boundary])
  
  subprocess.call('rm ' + filename, shell=True)

#Write the urls out
with open('randolph_boundaries.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(boundaries)
csvfile.close()

