OMG the readme website has a readme file no way thats crazy!!!! 🤪

# Setup
For a more comprehensive setup guide look at the pinned repo  
Make sure you have python installed  
Run these commands (if they don't work as a block just copy and paste them one by one)  


Linux:
```
git clone https://github.com/cmureadme/readme-website  # get code
cd readme-website  # enter the repo directory 
git checkout dev  # use the /dev branch
python3 -m venv venv  # create a virtual environment
source venv/bin/activate  # activate the virtual environment
pip install -r requirements.txt  # install libraries into the activated venv
chown u+x ./data_populate.sh # make shell script to do data set up executable
./data_populate.sh # run shell script to populate data
python3 manage.py runserver  # start the server
```

Windows:
```
git clone https://github.com/cmureadme/readme-website  # get code
cd readme-website  # enter the repo directory 
git checkout dev  # use the /dev branch
python -m venv venv  # create a virtual environment
venv\Scripts\activate  # activate the virtual environment
pip install -r requirements.txt  # install libraries into the activated venv
./data_populate.ps1 # run powershell script to populate data
python manage.py runserver  # start the server
```

# Helping
We have an issues page. You can read it and see if you know how to tackle one of the problems. 
You can can also whine on the issues page and someone else can then fix stuff for you. 
There are a lot of smart technical people in the discord. 
Talk in any of the website channels to get their help. 
Please follow the style guide in our pinned repo. 
Make sure that you are on the dev branch when making changes.

# File System
Most of our html and css files are named the same things so it should be pretty obvious what is paired with what.
All html files (except for base) should be in the templates\articles folder.
All css files should be in the styles folder.

## base.html and base.css
These files are the styling for the header this is at the top of nearly every page. 
Every other html file extends base, or a html file that extends base (denoted by {% extends "base.html" %} at the top of the file).
The styling in bass.css is the defalt styling applied to all pages.

## index.html and index.css
These files are for the front page of the website.

## about_us.html and about_us.css
The about us page.

## article_card.html and article_card.css
Used whenever a long list of articles are displayed on screen.
This should never have extends base.html at the top, instead this html page is included in other html pages.
Because this page is always included in other pages, the page that incudes this must have in its head include article_card.css (do not include the css in the html file as then on every call to this file (which is a lot) it has to also load the css, this is slow and bad practice).

## article_page.html and article_page.css
Actual page of an article.

## author_list.html and author_list.css
List of all the authors.
This is what you see when you click the staff tab.
Note that all staff are refered to as authors by our codebase.

## author.html and author.css
Page for a singluar staffmember.

## category.html
?????????? - rtosh or wade write this

## categorylist.html and category_list.css
NOTE categorylist should be renamed category_list
???????????? - rtosh or wade write this

## index_article_card.html
???? -rtosh or wade write this

## index_largest.html
??? rtosh or wade write this

## issue_list.html and issue_list.css
Our archives.
Under the issue tab on the website.

## issue.html
??????? rtosh or wade

## wrapper.css
???? rtosh write this
