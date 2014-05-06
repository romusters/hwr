
import os
from xml.dom import minidom
from PIL import Image
import time
#for saving file fast as binary data. Large files can be saved and loaded faster. File is 200 mb now.
import pickle
import shutil
from sklearn.cluster import KMeans
import math

import glob
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def read_all_pixels():
	all_pixels = []
	dir = "/home/pc/hwr/word_images/"
	pickle_pixels_file = "/home/pc/hwr/pixels.p"

	if not os.path.isfile(pickle_pixels_file):
		for file in os.listdir(dir):
			if file.endswith(".ppm"):
				image = Image.open(dir + file)
				width, height = image.size

				for x in range(width):
				    for y in range(height):
				        pixel = image.getpixel((x, y))
				        all_pixels.append(pixel)
		pickle.dump(all_pixels, open(pickle_pixels_file, "wb"))
	elif not os.path.isfile("/dev/shm/pixels.p"):
		shutil.copyfile(pickle_pixels_file, "/dev/shm/pixels.p") #/dev/shm/ is a directory which is not on the hard drive but in the ram memory which is faster.
	else:
		all_pixels = pickle.load(open("/dev/shm/pixels.p", "rb")) 
	return all_pixels


#cluster the RGB pixel values and compute centroids to which each pixel can be compaired
def compute_centroids():
	all_pixels = []
	ALL_DONE = 1
	while ALL_DONE:
		if not os.path.isfile("/dev/shm/pixels.p"):
			all_pixels = read_all_pixels()
		elif not os.path.isfile("/dev/shm/small_amount_of_pixels.p"):
			all_pixels = read_all_pixels()
			pickle.dump(all_pixels[0:2000000], open("/dev/shm/small_amount_of_pixels.p", "wb"))
		else:
			all_pixels = pickle.load(open("/dev/shm/small_amount_of_pixels.p", "rb")) 
			ALL_DONE = 0
			#set 3 clusters: 1 for letters, 1 for background and 1 for noise
			km = KMeans(3, n_jobs=2).fit(all_pixels)

			print "Length of pixels list is: ", len(all_pixels)

			cluster1 = tuple(km.cluster_centers_[0])#(222.31129101582974, 212.40518991275974, 196.93359071666441)
			cluster2 = tuple(km.cluster_centers_[1])#(125.49630215744433, 91.092558616599888, 74.036821559566391) <-winning, letters
			cluster3 = tuple(km.cluster_centers_[2])#(190.18255191113508, 172.47619816046111, 153.05295486366583)
			print "clusters", cluster1, cluster2, cluster3

			im = Image.new("RGB", (600, 600), "white")
			im.paste((int(cluster1[0]), int(cluster1[1]), int(cluster1[2])), (0,0,200,200)) 	
			im.paste((int(cluster2[0]), int(cluster2[1]), int(cluster2[2])), (200,200,400,400)) 
			im.paste((int(cluster3[0]), int(cluster3[1]), int(cluster3[2])), (400,400,600,600)) 
			#inspect which cluster contains the color of the letters.
			im.show()
			return cluster1, cluster2, cluster3

def main():
	#compute_centroids()
	files = glob.glob("/home/pc/hwr/word_images/*.ppm")
	letter_cluster 		= (222.31129101582974, 212.40518991275974, 196.93359071666441)
	background_cluster 	= (125.49630215744433, 91.092558616599888, 74.036821559566391)
	noise_cluster 		= (190.18255191113508, 172.47619816046111, 153.05295486366583)
	clusters = [letter_cluster, background_cluster, noise_cluster] #winning cluster has to be element 0
	
	DEVNULL = open(os.devnull, 'wb')

	try:
	    os.stat("/home/pc/hwr/kmeans_binary_words/")
	except:
	    os.mkdir("/home/pc/hwr/kmeans_binary_words/") 


	for file in files:
		image = Image.open(file)
		width, height = image.size

		result = []
		letter_pixels = []
		im = Image.new("1", (width, height), "white")
		array = np.zeros((width, height))
		for x in range(width):
			for y in range(height):
				pixel = image.getpixel((x, y))
				for e in clusters:
					result.append(math.pow(pixel[0] - e[0],2) + math.pow(pixel[1] - e[1],2) + math.pow(pixel[2] - e[2],2))
				if not result.index(min(result)) is 0:
					im.putpixel((x,y), 1)
					array[x][y] = 1
				result = []
		
		
		im.show()

		for x in range(width):
			for y in range(height):
				if array[x][y] is 255:
					array[x][y] = 0

		y=np.sum(array,0)
		x=np.sum(array,1)
		
		plt.plot(x)
		plt.plot(y)
		plt.show()

		#im.save("/home/pc/hwr/kmeans_binary_words/" + file.strip("/home/pc/hwr/word_images/"), "png")
		time.sleep(0.5)
		subprocess.call(["killall", "-9", "display"])



if __name__ == "__main__":
    main()
