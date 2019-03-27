#This file creates a file of urls pertaining to randolph county only
import csv
import numpy as np
import subprocess

#Import urls
urlfile = open('tile_urls.csv')
raw_urls = list(csv.reader(urlfile))[0:]
urls = [item for sublist in raw_urls for item in sublist]

randolph_urls = list()

#Trim the list to only refer to randolf county
for url in urls:
  if("Randolph" in url):
    randolph_urls.append([url])

#Write the urls out
with open('randolph_tile_urls.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(randolph_urls)
csvfile.close()


#print(len(randolph))
