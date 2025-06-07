python manage.py migrate  # create the blank database file
python manage.py loaddata db_sample.json  # populate it with sample data

Expand-Archive -Path "zips\media.zip" -DestinationPath "."

# Article Image folder was too large for one zip file so I split it into two
# folders to upload it to the github this auto merges them back
Expand-Archive -Path "zips\vol3.zip" -DestinationPath "media"
Expand-Archive -Path "zips\author_images.zip" -DestinationPath "media"

Expand-Archive -Path "zips\article_images1.zip" -DestinationPath "."
Expand-Archive -Path "zips\article_images2.zip" -DestinationPath "."

Move-Item -Path "article_images1\*" -Destination "media\article_images"
Move-Item -Path "article_images2\*" -Destination "media\article_images"

Remove-Item "article_images1"
Remove-Item "article_images2"