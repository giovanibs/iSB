import inspect
from time import sleep, time
import C
import re

def search(cro, search_term, timeout=30):
    
    print('Searching for inputed terms...')
    
    search_term = search_term.replace(" ", "+")
    results_order = C.RESULTS_ORDER["Ending soon"]
    url = f"https://www.binance.com/en/nft/search-result?keyword={search_term}&tab=nft&order={results_order}"
    
    return load_results(cro, url)
    
def load_results(cro, url, timeout=30):
    
    cro.get(url)

    ### CHECK WHETHER THE RESULTS HAVE BEEN LOADED
    t0 = time()
    results_have_loaded = False
    
    while not results_have_loaded:

        # css-4tart7 >>> loading element

        try:  # check if the "no items" element has been displayed in the results
            no_items = cro.find_element_by_class_name("css-17zmp1k")

            if no_items.text == "No items":
                return False

        except:  # if not, try getting he number of results found
            print(
                "It looks like we've got some results (or the page hasn't loaded yet...)"
            )
            sleep(1)
        
        try: 
            search_results_msg = cro.find_element_by_class_name("css-15u79n8").text
        except:
            search_results_msg = cro.find_element_by_class_name("css-ujlbbb").text
            
        results_found = int(search_results_msg.split(" ")[1])
        
        # in case the web elements haven't loaded, we may get a 0 for results_found
        if results_found == 0:
            continue  # jumps the code below until "no_items" OR "results_found" is True

        # ok, we've got results, let's check if they've finished loading
        # the search returns, initizally, the first 16 results
        # try getting the last loaded result's 'Creator' element
        
        if results_found > 16:
            last_loaded_result_index = 15
        else: 
            last_loaded_result_index = results_found - 1
        
        try:
            results_have_loaded = (
                cro.find_elements_by_class_name("css-1ez451f")[last_loaded_result_index].text == "Creator"
                )
            return True
        except:
            sleep(1)

        ### TIMEOUT!
        elapsed_time = time() - t0
        if elapsed_time > timeout:
            this_func = inspect.stack()[0][3]
            print(f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}")
            return False

def order_results(cro, order_option=1):

    if not (int(order_option) in C.ORDER_OPTIONS):
        print(f"Choose a valid option:{list(C.ORDER_OPTIONS.keys())}")
        return

    order_by = C.ORDER_OPTIONS[int(order_option)]
    results_order = C.RESULTS_ORDER[order_by]

    # keep current search url and change only the order parameter
    current_search = cro.current_url.split("&order=")[0]
    url = f"{current_search}&order={results_order}"

    return load_results(cro, url)

def read_results(cro):
    try:
        results = cro.find_elements_by_class_name(C.RESULT_DIV)
        1/len(results)
    except:
        results = cro.find_elements_by_class_name(C.RESULT_DIV_SMALL_SCREEN)
        
    results_list = []
    
    
    for result in results:
        
        result_info_list = result.text.split("\n")
        print(f"read_results infos: {len(result_info_list)}")
        
        result_obj = {}
        # if the NFT is not currently in auction, there will be no remaining time element
        if len(result_info_list) == 8:
            
            for index, label in enumerate(C.RESULT_INFOS_WO_REMAINING_TIME):
                result_obj[label] = result_info_list[index]
        
        elif len(result_info_list) == 10:
            
            for index, label in enumerate(C.RESULT_INFOS_WITH_REMAINING_TIME):
                result_obj[label] = result_info_list[index]
        
        try:
            result_imgs = result.find_elements_by_tag_name("img")  # result div has 3 imgs
            #print("imagens encontradas: ", len(result_imgs))
            result_obj["img_preview"] = result_imgs[0].get_attribute('src')  
            #result_obj["currency_thumbnail"] = result_imgs[1].get_attribute('src')
            #result_obj["creator_thumbnail"] = result_imgs[2].get_attribute('src')
        
        except Exception as e:
            print(f"Algo deu errado ao obter infos dos resultados: {e}")
            return 0
        
        results_list.append(result_obj)
    return results_list

def print_results(results_list, max_results=5):

    print("Here are the top 5 NFTs encountered:\n(...)")

    for result_index, result in enumerate(results_list):
        
        print(f'\n\n{18*"#"}')
        for key, info in result:
            print ( f"{key}: {info}" )
        print(f'\n\n{18*"#"}')
        
        # print(
        #     f'\n\n{18*"#"}',
        #     f'title: { result["title"] }',
        #     f'img_src: { result["img_src"] }',
        #     f'price: { result["price"] }',
        #     f'price_in_current_currency: { result["price_in_current_currency"] }',
        #     f'creator_name: { result["creator_name"] }',
        #     f'creator_thumbnail: { result["creator_thumbnail"] }',
        #     f'{18*"#"}',
        #     sep="\n",
        # )
        if result_index == max_results - 1:
            break

def search_for_terms(cro, search_term, timeout=10):

    ######### search_input element is not visible for width < 1023 #########
    small_window = cro.get_window_size()["width"] < 1023
    if small_window:
        t0 = time()
        open_search_button = 0
        while not open_search_button:
            try:
                open_search_button = cro.find_element_by_class_name("css-43igg3")
                open_search_button.click()
            except:  # TIMEOUT!
                elapsed_time = time() - t0
                if elapsed_time > timeout:
                    this_func = inspect.stack()[0][3]
                    f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
                    return 0
                sleep(1)

    ######### WAIT FOR INPUT FIELD TO BE AVAILABLE #########
    t0 = time()
    search_input = 0

    while not search_input:
        try:
            search_input = cro.find_element_by_class_name("css-16fg16t")
            search_input.send_keys(search_term)
        except:  # TIMEOUT!
            elapsed_time = time() - t0
            if elapsed_time > timeout:
                this_func = inspect.stack()[0][3]
                f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
                return 0
            sleep(1)

    ## search_button element differs depending on screen size
    search_button_class = "css-npwchv" if small_window else "css-1p3lb33"

    t0 = time()
    search_input = 0

    while not search_input:
        try:
            search_button = cro.find_element_by_class_name(search_button_class)
            search_button.click()
            return 1
        except:  # TIMEOUT!
            elapsed_time = time() - t0
            if elapsed_time > timeout:
                this_func = inspect.stack()[0][3]
                f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
                return 0
            sleep(1)

def accept_terms(cro, timeout=30):
    print('Accepting terms...')
    t0 = time()
    accept_terms_button = 0

    while not accept_terms_button:
        try:
            accept_terms_button = cro.find_element_by_class_name("css-5slqk3")
            accept_terms_button.click()
            print('Terms accepted...')
            return 1

        except:
            elapsed_time = time() - t0
            if elapsed_time > timeout:
                this_func = inspect.stack()[0][3]
                f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
                return 0
            sleep(1)

# def got_search_results(cro, timeout=30):
#     t0 = time()
#     #search_results_msg = "empty"
#     #regex = re.compile(C.GOT_RESULTS)
#     results_found = 0
#     while not results_found:       # bool(re.match(regex, search_results_msg)):
#         try:
#             search_results_msg = cro.find_element_by_class_name("css-15u79n8").text
#             results_found = search_results_msg.split(" ")[1]
#         except:
#             search_results_msg = cro.find_element_by_class_name("css-ujlbbb").text
#             results_found = search_results_msg.split(" ")[1]
        
#         # TIMEOUT!
#         elapsed_time = time() - t0
#         if elapsed_time > timeout:
#             this_func = inspect.stack()[0][3]
#             f"\n\n{18*'#'}\nTimeout...{this_func}\n{18*'#'}"
#             return 0
#         sleep(1)

#     return results_found
