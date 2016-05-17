import zipfile
import os.path
from PIL import Image
import sys
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="Zip FILE to unzip and add thumbnails", metavar="FILE")
parser.add_argument("-p", "--path", dest="file_path",
                    help="Zip FILE PATH ", metavar="FILE_PATH")

# Upload Directory for Zip Files
zip_file_path = os.getcwd()
main_image_path = '/www/public_html/admin/images/media/product/main/new/'
thumbnail_image_path = '/www/public_html/admin/images/media/product/thumbnails/new/'

# Thumbnail Size
size = 150, 150


def upload_image(file_path, filename):
	zip_file_path = os.getcwd() + file_path
	print "Zip File Path : %s"%(zip_file_path + filename)
	zfile = zipfile.ZipFile(zip_file_path + filename)
	for name in zfile.namelist():
		(dirname, filename) = os.path.split(name)
		zfile.extract(filename, main_image_path)
		new_filename = filename.replace(" ","_")
		os.rename(main_image_path + filename, main_image_path + new_filename)
		# Creating Thumbnail
		try:
			im = Image.open(main_image_path + new_filename)
			im.thumbnail(size, Image.ANTIALIAS)
			im.save(thumbnail_image_path + new_filename, "JPEG")
		except IOError:
			print "cannot create thumbnail for %s on location : %s" % (main_image_path + new_filename, thumbnail_image_path + new_filename)
			print sys.exc_info()
		
args = parser.parse_args()

upload_image(args.file_path, args.filename)
