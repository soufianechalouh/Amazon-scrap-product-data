import csv
import time
import uuid

import os
import lxml
from zipfile import ZipFile

from flask import send_from_directory
from selectorlib import Extractor
from selenium import webdriver


def get_assins(file_name):
    unique_ext = uuid.uuid4().hex[:6].upper()
    unique_output = "{}_output.csv".format(unique_ext)
    driver = get_chromedriver("./chromedriver2")

    with open(os.path.join('tmp/uploads', file_name)) as csv_file, \
            open(os.path.join('tmp/downloads', unique_output), 'w') as outfile:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                url = row[0]
                data = scrape(driver, "{}".format(url))
                print("{},{}\n".format(url, str(data['seller']).replace("Brand: ", "")))
                outfile.write("{},{}\n".format(url, str(data['seller']).replace("Brand: ", "")))

                line_count += 1

                # SET Time between every 2 crawlings

                time.sleep(1)
        print(f'Processed {line_count} lines.')

    # The rest if this function represents post-processing and exporting results as a zip file
    download_name = "{}_processed".format(unique_ext)
    driver.close()
    time.sleep(2)
    # with ZipFile('./tmp/downloads/'+download_name+'.zip', 'w') as zip:
    with ZipFile(os.path.join('tmp/downloads', download_name + '.zip'), 'w') as zip:
        # writing each file one by one
        zip.write(os.path.join('tmp/downloads', unique_output))

    return send_from_directory('tmp/downloads', download_name + '.zip')

    # return redirect(url_for("download", filename=download_name + '.zip'), 200)


def scrape(driver, url):
    e = Extractor.from_yaml_file('./static/selectors.yml')
    driver.get(url)
    return e.extract(driver.page_source)


def get_chromedriver(chrome_driver_location):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-agent=%s' % user_agent)
    # Comment the following line to see it at work
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(executable_path=chrome_driver_location, options=chrome_options)