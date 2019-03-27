#This file writes out all the urls of the IN LIDAR raster tiles
import requests
from lxml import html
import csv

#Base URLs
east_url = "https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/IN_2011_2013_E/IN_2011_2013_E_be/"
west_url = "https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/IN_2011_2013_W/IN_2011_2013_W_be/"

#Tile List
tile_urls = list()

#Get the east county dataset
east = requests.get(east_url)
east_tree = html.fromstring(east.content)
east_counties = east_tree.xpath('//tr[@class="item subdir"]/td[@class="colname"]/a/text()')
#trim an extra dir off the list
for county in east_counties:
  print(county)
  county_html = requests.get(east_url+county)
  county_tree = html.fromstring(county_html.content)
  county_tiles = county_tree.xpath('//tr[@class="item type-application type-octet-stream"]/td[@class="colname"]/a/text()')
  for tile in county_tiles:
    tile_url = east_url + county + tile
    tile_urls.append([tile_url])

#Get the west county dataset
west = requests.get(west_url)
west_tree = html.fromstring(west.content)
west_counties = west_tree.xpath('//tr[@class="item subdir"]/td[@class="colname"]/a/text()')
for county in west_counties:
  print(county)
  county_html = requests.get(west_url+county)
  county_tree = html.fromstring(county_html.content)
  county_tiles = county_tree.xpath('//tr[@class="item type-application type-octet-stream"]/td[@class="colname"]/a/text()')
  for tile in county_tiles:
    tile_url = west_url + county + tile
    tile_urls.append([tile_url])

#Write the urls out
with open('tile_urls', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(tile_urls)
csvfile.close()

#print(len(tile_urls))
#print(len(set(tile_urls)))
#print(tile_urls[25000])


