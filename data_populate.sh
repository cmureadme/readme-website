#!/usr/bin/bash

set -e

python3 manage.py makemigrations
python3 manage.py migrate  # create the blank database file
python3 manage.py loaddata db_sample.json  # populate it with sample data

cd zips/
unzip media.zip -d ../ # creates and populate the media folder

# Article Image folder was too large for one zip file so I split it into two
# folders to upload it to the github this auto merges them back
unzip vol3.zip -d ../media
unzip author_images.zip -d ../media

unzip article_images1.zip
unzip article_images2.zip

mv article_images1/* ../media/article_images
mv article_images2/* ../media/article_images

rmdir article_images1
rmdir article_images2
