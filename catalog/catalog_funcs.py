import const
import xmltodict
import requests as rq
import json
from os import path


def save_nft_from_catalog_list(list_key):
    catalog = open_local_catalog_list()
    
    if (list_key > len(catalog)):
        return
    
    nft_key = catalog[list_key][const.KEY]
    
    # check if it's a nft
    if nft_key not in const.NFT_PATH:
        return
    
    # check file extension
    if nft_key.split('.')[-1] not in const.NFT_FORMATS:
        return
    
    nft_file_name = path.join(const.SAVE, nft_key.split('/')[-1])
    
    # check if file already exists in dir
    if path.exists(nft_file_name):
        return
    
    image_url = const.BASE_URL + nft_key
    img_data = rq.get(image_url).content

    # save img
    with open(nft_file_name, 'wb') as img:
        img.write(img_data)

def open_local_catalog_list():
    
    with open("catalog.json", 'r') as f:
        json_catalog = f.read()
    
    catalog = json.loads(json_catalog)[const.LIST_BUCKET][const.CONTENT]
    
    return catalog

def get_local_catalog_bucket():
    
    with open("catalog.json", 'r') as f:
        json_catalog = f.read()
    
    catalog_bucket = json.loads(json_catalog)[const.LIST_BUCKET]
    
    return catalog_bucket

def get_catalog():
    '''Gets NFT catalog from https://public.nftstatic.com/
    and saves it as a JSON file
    '''
    url = r"https://public.nftstatic.com/"

    r = rq.get(url)
    html_txt = r.text

    catalog = xmltodict.parse(html_txt)

    catalog = json.dumps(catalog)

    with open("catalog.json", 'w') as f:
        f.write(catalog)