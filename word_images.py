# -*- coding: utf-8 -*-
import os
from xml.dom import minidom
from PIL import Image
import time

def main():
	#find directory where the pages and words are.
	first_part_of_filename = find_data_dir()

	#read all the images, extract the words in the image as files and save files.
	for index in range(6,54,2):
		if index < 10:
			index = "0" + str(index)
		filename_image  = first_part_of_filename + "pages/KNMP/KNMP-VIII_F_69______2C2O_00"  + str(index) + ".jpg"
		filename_words = first_part_of_filename + "words/KNMP/KNMP-VIII_F_69______2C2O_00" + str(index) + ".words"

		image = Image.open(filename_image)

		xml = minidom.parse(filename_words)
		word_list = xml.getElementsByTagName('Word')

		for e in word_list:
			area = image.crop((int(e.attributes["left"].value), int(e.attributes["top"].value), int(e.attributes["right"].value), int(e.attributes["bottom"].value)))
			word_image_dir = "/home/pc/hwr/word_images/"
			try:
			    os.stat(word_image_dir)
			except:
			    os.mkdir(word_image_dir) 

			area.save(word_image_dir + "KNMP-VIII_F_69______2C2O_00"  + str(index) + "_" + str(e.attributes["no"].value) + "_" + str(e.attributes["text"].value) + ".ppm", "ppm")

#1095 230 1136 277
#left, 

def find_data_dir():
	for dirname, dirnames, filenames in os.walk('/'):
		if "data" in dirnames:
			return dirname + "/data/" 
				



if __name__ == "__main__":
    main()