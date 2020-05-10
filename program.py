@@ -0,0 +1,61 @@
from bottle import route, run, template
import requests
from bs4 import BeautifulSoup
import csv

with open('newsletter_data.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    data = {}
    for row in reader:
        for header, value in row.items():
            try:
                data[header].append(value)
            except KeyError:
                data[header] = [value]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
references = data["referencje"]
images = data["grafiki"]
images_links = data["linki"]
text = data["tekst"]
product_names = []
product_images = []
product_urls = []
x = int(0)

while x < 9:
    product_search_url = requests.get("https://jubitom.com/szukaj?submit_search=&controller=search&orderby=position&orderway=desc&search_query=" + str(references[x]), headers=headers)
    source = product_search_url.content
    soup = BeautifulSoup(source, 'html5lib')

    product_name = soup.find(itemprop="url")
    product_names.append(product_name["title"])

    product_image = soup.find(itemprop="image")
    product_images.append(product_image["data-src"])

    product_url = soup.find(itemprop="url")
    product_urls.append(product_url["data-href"].split("?", 1)[0])

    x += 1

print(product_names)
print(product_images)
print(product_urls)
print(images)
print(images_links)
print(text)


@route('/newsletter')
def newsletter():
    return template('newsletter',
                    product_names=product_names,
                    product_urls=product_urls,
                    product_images=product_images,
                    images=images,
                    images_links=images_links,
                    text=text)


run(host='localhost', port=8080, debug=True)
