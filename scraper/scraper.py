import numpy as np 
import pandas as pd
import requests
from bs4 import BeautifulSoup

# find data
def scrape_product_detail_page(product_detail_url):

    # scrape data
    res = requests.get(product_detail_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # model is in the title
    model = soup.title.text
    
    # url
    url = soup.select('a')[0].get('href') 
    
    # preprocess image data, we are looking for img with alt model
    # condition for missings, even though main photo should always be present
    image_data = []
    images = soup.select('img')
    
    for image in images:
        src = image.get('src')
        alt = image.get('alt')
        if alt == soup.title.text:
            image_data.append(src)
    
    main_photo_path = (image_data[0] if image_data else None)
    additional_photo_paths = (image_data[1:] if image_data else None)
    
    # price
    # soup.select('div.cena')[0].text.strip().split('\n')[0]
    price = int(soup.find('input', attrs={'name':'cena_obj'}).get('value'))
    
    # preprocess spec
    # find all tables (there are two 'spec' tables, we need both)
    tables = soup.findAll("table") # a list of tables
    
    specifics_list = []
    
    # get a list of each element (list of lists)
    for table in tables:
        specifics_list.append(table.find_all('td'))
    
    # flatten the list to get rid of list of lists
    flat_list = [item for sublist in specifics_list for item in sublist]
    
    # create empty lists and fill based on condition
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
    
    # select first value + add condition for None
    model_year = int(model_year_prep[0])
    weight = (weight_prep[0] if weight_prep else None)
    frame = (frame_prep[0] if frame_prep else None)
    
    # create parameters dictionary
    class NewClass(object): pass
    parameters = NewClass()
    vars = ['weight', 'frame']
    for v in vars: 
        setattr(parameters, v, eval(v)) 
        
    # create final dictionary
    class NewClass(object): pass
    final_dataset = NewClass()
    cols = ['model', 'url', 'main_photo_path', 
            'additional_photo_paths', 'price', 
            'model_year']
    for c in cols: 
        setattr(final_dataset, c, eval(c)) 
        
    # nest parameters into final dataset
    final_dataset.__dict__['parameters'] = parameters.__dict__

    return final_dataset.__dict__