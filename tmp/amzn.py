import csv
import time
import uuid

from bs4 import BeautifulSoup
import os
import lxml
from zipfile import ZipFile

from flask import url_for
from selectorlib import Extractor
import requests


def get_assins(file_name):


    unique_ext = uuid.uuid4().hex[:6].upper()
    unique_output = "/tmp/downloads/{}_output.csv".format(unique_ext)

    with open("/tmp/uploads/"+file_name) as csv_file, open(unique_output, 'w') as outfile:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                url = row[0]
                data = scrape("{}".format(url))
                outfile.write("{},{}\n".format(url, str(data['seller']).replace("Brand: ", "")))

                line_count += 1
                time.sleep(1)
        print(f'Processed {line_count} lines.')

    # The rest if this function represents post-processing and exporting results as a zip file
    download_name = "{}_processed".format(unique_ext)

    with ZipFile('./tmp/downloads/'+download_name+'.zip', 'w') as zip:
        # writing each file one by one
        zip.write(unique_output)

    # return send_from_directory('tmp', 'my_python_files.zip')

    tempUrl = "http://127.0.0.1:5000"+url_for("download", filename=download_name+'.zip')
    response = {"download_link": tempUrl}
    return response


def scrape(url):

    e = Extractor.from_yaml_file('selectors.yml')
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" %url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)
