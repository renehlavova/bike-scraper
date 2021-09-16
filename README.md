# bike-scraper

`bike-scraper` is a tiny scraping project in Python (Python 3.9). 

It returns a dictionary from Lapierre bicycles https://www.lapierre-bike.cz with a function:
```
def scrape_product_detail_page(product_detail_url):
        pass
```

It has following specifics:
* `model` - string, title
* `url` - string
* `main_photo_path` - path to the main photo with the biggest size
* `additional_photo_paths` - other paths of the photos
* `price` - integer
* `model_year` - integer, to be found under "Ročník in section "spec"

It also contains a nested section `parameters` with the following specs: 
* `weight` - string, to be found under "Hmotnost" in section "spec" 
* `frame` - string, to be found under "Rám" in section "spec" 
