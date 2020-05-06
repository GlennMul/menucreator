import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


# noinspection PyBroadException
def get_menu(url):
    main_url = 'https://www.ubereats.com'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    r = requests.get(url, headers=hdr, timeout=15)
    doc = BeautifulSoup(r.text, "html.parser")

    cat_list = []
    dish_list = []
    desc_list = []
    price_list = []
    pic_list = []

    category = doc.select('li')

    for item in category:
        try:
            cat_name = item.select('h2')[0].text
        except:
            cat_name = cat_name

        card = item.select('ul li')

        for i in card:
            cat_list.append(cat_name)
            dish_list.append(i.select('h4')[0].text.strip())
            splash = main_url + i.select('a')[0].attrs['href'].strip()
            try:
                desc_list.append(i.select('.c6')[0].text.strip())
            except:
                desc_list.append(np.NaN)
            try:
                price_list.append(i.select('.b8')[1].text.strip())
            except:
                price_list.append(np.NaN)
            try:
                picr = requests.get(splash, headers=hdr, timeout=15)
                pic = BeautifulSoup(picr.text, "html.parser")
                pic_list.append(pic.select('.af.d2 img')[0].attrs['src'])
            except:
                pic_list.append(np.NaN)

    data = {'Category': cat_list,
            'Menu_Item': dish_list,
            'Description': desc_list,
            'Price': price_list,
            'Pic_URL': pic_list}
    df = pd.DataFrame(data)

    return df
