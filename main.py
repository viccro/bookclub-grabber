#!/usr/local/bin/python3

import csv
import os
import requests
import sys
import time
import xml.etree.ElementTree as ET

google_books_api_url = "https://www.googleapis.com/books/v1/volumes?q="
goodreads_api_url = "https://www.goodreads.com/search/index.xml"
goodreads_key = os.environ.get('GOODREADS_API_KEY')

def main(csv_path):
    with open(csv_path, newline='') as csvfile:
        filereader = csv.DictReader(csvfile)
        for row in filereader:
            callGoodreadsApi(row)
            callGoogleApi(row)
            time.sleep(8)


def callGoogleApi(row):
    unescaped_data = str(row['Title']) # + ' ' + str(row['Author Editor'])

    plus_escaped_data = unescaped_data.replace(' ','+')
    response = requests.get(google_books_api_url+plus_escaped_data)

    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request: '+ plus_escaped_data)

    else:
        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        topResult = data['items'][0]['volumeInfo']

        try:
            pages = topResult['pageCount']
            #find that page length
            print("Page count: " + str(pages))
        except Exception as e:
            print(e)
            print(topResult)
    if row['Why']:
        print("Why are you nominating this book?: " + str(row['Why']))
    print("\n")


def callGoodreadsApi(row):
    unescaped_data = str(row['Title']) #   + ' ' + str(row['Author'])

    plus_escaped_data = str(unescaped_data.replace(' ','+'))

    response = requests.get(goodreads_api_url + "?key=" + goodreads_key + "&q=" + plus_escaped_data)

    if response.status_code != 200:
        print('Status:', str(response.status_code), 'Problem with the request: '+ (plus_escaped_data))

    root = ET.fromstring(response.text)

    try:
        book = root.find('search').find('results').find('work').find('best_book')
        #print(book.results)
        title = book.find('title').text
        id = book.find('id').text
        authors = []
        for person in book.findall('author'):
            authors.append(person.find('name').text)
        url = str("https://www.goodreads.com/book/show/" + id)
        rating = str(root.find('search').find('results').find('work').find('average_rating').text)
        pub_year = str(root.find('search').find('results').find('work').find('original_publication_year').text)
        num_ratings = str(root.find('search').find('results').find('work').find('ratings_count').text)

        print("Title: " + title)
        print("Author: " + ",".join(authors))
        print("Publication year: " + pub_year)
        print("Goodreads: " + url)
        print("Goodreads rating: " + rating + " (from " + num_ratings + " ratings)")
    except Exception as e:
        print(e)
        print(unescaped_data)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the csv input")
