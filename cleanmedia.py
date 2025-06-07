"""
Luke's very genius script to delete article images we don't need
"""

import sqlite3
import os

folder_path = r"media/article_images"

try:
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("SELECT image FROM articles_articleimage")
    results = cursor.fetchall()
    cleaned_results = list()

    for row in results:
        row_str = str(row)
        cleaned_results.append(str(row_str[row_str.index("/") + 1 : row_str.index("',)")]))
    print ("Rows cleaned")
    
    for filename in os.listdir(folder_path):
            if str(filename) in cleaned_results:
                print ("Kept " + filename)
            else:
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"{filename} is removed")
    
    
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if connection:
        connection.close()
        print("The SQLite connection is closed")