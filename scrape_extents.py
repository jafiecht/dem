import numpy as np
import requests
import subprocess
import csv
import json
import pandas

#Import tile urls
urlfp = 'tile_urls.csv'
outfp = 'boundaries.csv'
urlfile = pandas.read_csv(urlfp, header=None)
extentfile = pandas.read_csv(outfp, header=None)
urlfile = urlfile[~urlfile[0].isin(extentfile[0].values)]
urls = urlfile[0].tolist()

print(len(urls))
print(extentfile.shape)
print(urlfile.shape)

#Download the file
index = 1
for url in urls:
  #Download the raster tile
  tile = requests.get(url, allow_redirects=True)
  filename = url.rsplit('/', 1)[1]
  outfile = open(filename, 'wb')
  outfile.write(tile.content)
  outfile.close()

  try:
    #Get the extent
    raster_info = subprocess.check_output('gdalinfo -json ' + filename, shell=True)
    info = json.loads(raster_info.decode('utf8'))
    boundary = info["wgs84Extent"]["coordinates"][0]

    #Write the extent out
    with open(outfp, 'a') as outfile:
      writer = csv.writer(outfile)
      writer.writerow([url, boundary])
    outfile.close()

    print(index, 'Good')
    index += 1

  except:
    #Write out the dud url
    with open('dud_urls.csv', 'a') as outfile:
      writer = csv.writer(outfile)
      writer.writerow([url])
    outfile.close()

    print(index, 'No Good')
    index += 1

  #Remove the temporary file
  subprocess.call('rm ' + filename, shell=True)

