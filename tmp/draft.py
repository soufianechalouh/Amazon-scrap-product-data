import csv
import time

from bs4 import BeautifulSoup
import requests
from selectorlib import Extractor
import requests
import json
from time import sleep

e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):
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
    print("Downloading %s"%url)
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


file_name = "file.csv"


with open("./uploads/" + file_name) as csv_file, open('./downloads/output.csv', 'w') as outfile:
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
            # outfile.write(url + "," + data['seller'] + "\n")
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
            time.sleep(1)
    print(f'Processed {line_count} lines.')


# with open("urls.txt", 'r') as urllist, open('output.csv', 'w') as outfile:
#     for url in urllist.readlines():
#         data = scrape(url)
#         outfile.write(url+","+data['seller']+"\n")


# headers = {
#         'authority': 'www.amazon.com',
#         'pragma': 'no-cache',
#         'cache-control': 'no-cache',
#         'dnt': '1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'sec-fetch-site': 'none',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-dest': 'document',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     }
# source = requests.get('https://www.amazon.com/',headers=headers).text
#
# soup = BeautifulSoup(source, 'lxml')
# print(soup.prettify())

# with open('employee_birthday.txt') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#             line_count += 1
#     print(f'Processed {line_count} lines.')
