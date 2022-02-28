import catalog_funcs
import const
from os import path
import pandas as pd
import sys

catalog = catalog_funcs.open_local_catalog_list()

pd_catalog = pd.DataFrame(catalog)

print(pd_catalog['Size'].sum())

#total_size = pd_catalog.sum(axis='Size')
#print(total_size)

### EXIT ###
sys.exit()
############

nft_paths = []
nft_paths2 = []

for item in catalog:
    
    nft_base_path = path.split(item[const.KEY])[0] # static/nft/res/
    if not nft_base_path:
        continue
    
    nft_base_path2 = item[const.KEY].split('/')[:-1]
    nft_paths.append(nft_base_path)
    nft_paths2.append(nft_base_path2)

nft_paths = set(nft_paths)
nft_paths2 = set(nft_paths2)
print(nft_paths)
print(nft_paths2)


#for index in range(100):
#    nft_funcs.save_nft_from_catalog_list(index)