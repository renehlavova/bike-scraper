import json
import requests
from bs4 import BeautifulSoup

def scrape_product_detail_page(product_detail_url):
    bicycle = dict()
    parameters = dict()

    # scrape data
    res = requests.get(product_detail_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # model
    bicycle['model'] = soup.title.text
    
    # url
    bicycle['url'] = soup.select('a')[0].get('href') 
    
    # preprocess image data, we are looking for img with alt model
    # condition for missings, even though main photo should always be present
    image_data = []
    images = soup.select('img')
    
    for image in images:
        src = image.get('src')
        alt = image.get('alt')
        if alt == soup.title.text:
            image_data.append(src)
    
    bicycle['main_photo_path'] = (image_data[0] if image_data else None)
    bicycle['additional_photo_paths'] = (image_data[1:] if image_data else None)
    
    # price
    bicycle['price'] = int(soup.find('input', attrs={'name':'cena_obj'}).get('value'))
    
    # preprocess spec
    # find all tables (there are two 'spec' tables, we need both)
    tables = soup.findAll("table") 
    
    specifics_list = []
    
    for table in tables:
        specifics_list.append(table.find_all('td'))
    
    # flatten the list to get rid of list of lists
    flat_list = [item for sublist in specifics_list for item in sublist]

    model_year_prep = []
    weight_prep = []
    frame_prep = []
    
    for i, val in enumerate(flat_list):
        row = val.get_text(strip=True)
        if row == 'Ročník':
            model_year_prep.append(flat_list[i+1].get_text(strip=True))
        elif row == 'Rám':
            frame_prep.append(flat_list[i+1].get_text(strip=True))
        elif row == 'Hmotnost':
            weight_prep.append(flat_list[i+1].get_text(strip=True))
    
    bicycle['model_year'] = int(model_year_prep[0])
    parameters['weight'] = (weight_prep[0] if weight_prep else None)
    parameters['frame'] = (frame_prep[0] if frame_prep else None)
   
    # nest parameters into final dataset
    bicycle['parameters'] = parameters

    return bicycle

def main(name, urls):
    data = []
    for url in urls:
        data.append(scrape_product_detail_page(url))
    
    with open(name, 'w') as outfile:
        json.dump(data, outfile)
    
if __name__ == '__main__':
    urls = [
        'https://www.lapierre-bike.cz/produkt/spicy-cf-69/5943',
        'https://www.lapierre-bike.cz/produkt/lapierre-shaper-30-disc/6021',
        'https://www.lapierre-bike.cz/produkt/trekking-30/6011',
        'https://www.lapierre-bike.cz/produkt/overvolt-glp-elite-b500/5956',
        'https://www.lapierre-bike.cz/produkt/prorace-16-girl/5985'
    ]
    main("top-5-bikes.json", urls)
