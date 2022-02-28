import inspect
from time import sleep, time
import C
import re


def search(cro, search_term, timeout=30):
    search_term = search_term.replace(" ", "+")
    results_order = C.RESULTS_ORDER["Ending soon"]
    url = f"https://www.binance.com/en/nft/search-result?keyword={search_term}&tab=nft&order={results_order}"
    cro.get(url)

    ### CHECK WHETHER THE RESULTS HAVE BEEN LOADED
    t0 = time()
    is_loaded = 0
    while not is_loaded:

        try:  # check if the "no items" element has been displayed in the results
            no_items = cro.find_element_by_class_name("css-17zmp1k")

            if no_items.text == "No items":
                return 0

        except:  # if not, try getting he number of results found
            results_found = got_search_results(cro)

        # in case the web elements haven't loaded, we may get a 0 for results_found
        if results_found == 0:
            continue  # jumps the code below until "no_items" OR "results_found" is True

        # ok, we've got results, let's check if they've finished loading
        # try getting the last result's 'Creator' element
        while not is_loaded:
            try:
                if results_found > 16:
                    is_loaded = (
                        cro.find_elements_by_class_name("css-1ez451f")[15].text
                        == "Creator"
                    )
                else:
                    is_loaded = (
                        cro.find_elements_by_class_name("css-1ez451f")[
                            results_found - 1
                        ].text
                        == "Creator"
                    )
            except:
                sleep(1)

            ### TIMEOUT!
            elapsed_time = time() - t0
            if elapsed_time > timeout:
                this_func = inspect.stack()[0][3]
                f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
                return False

        ### TIMEOUT!
        elapsed_time = time() - t0
        if elapsed_time > timeout:
            this_func = inspect.stack()[0][3]
            f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
            return False

    return True


def order_results(cro, order_option=1):

    if not (int(order_option) in C.ORDER_OPTIONS):
        print(f"Choose a valid option:{list(C.ORDER_OPTIONS.keys())}")
        return

    order_by = C.ORDER_OPTIONS[int(order_option)]
    results_order = C.RESULTS_ORDER[order_by]

    # keep current search url and change only the order parameter
    current_search = cro.current_url.split("&order=")[0]
    url = f"{current_search}&order={results_order}"

    cro.get(url)


def read_results(cro):

    #
    results = cro.find_elements_by_css_selector(C.RESULT_DIV)
    results_list = []
    print("Here are the top 5 NFTs encountered:\n(...)")
    for result in results:
        result_obj = {
            "img_src": result.find_element_by_tag_name(
                "img"
            ).src,  # result div has 3 imgs
            "title": result.find_element_by_class_name(
                "css-z6gv93"
            ),  # div class="css-z6gv93"
            "price": result.find_element_by_class_name(
                "css-rjqmed"
            ),  # div class="css-rjqmed"
            "price_in_current_currency": result.find_element_by_class_name(
                "css-zsxp4z"
            ),  # span class="css-zsxp4z"
            #'creator_div' : result.find_element_by_class_name("css-crf5wt"),                # div class="css-crf5wt"
            "creator_name": result.find_element_by_class_name(
                "css-7v9a5f"
            ),  # div class="css-7v9a5f"
            "creator_thumbnail": result.find_element_by_tag_name(
                "img"
            ).src,  # img class="css-me5nem"
        }
        results_list.append(result_obj)
    return results_list


def print_results(results_list, max_results=5):

    print("Here are the top 5 NFTs encountered:\n(...)")

    for result_index, result in enumerate(results_list):
        print(
            f'\n\n{18*"#"}',
            f'title: { result["title"] }',
            f'img_src: { result["img_src"] }',
            f'price: { result["price"] }',
            f'price_in_current_currency: { result["price_in_current_currency"] }',
            f'creator_name: { result["creator_name"] }',
            f'creator_thumbnail: { result["creator_thumbnail"] }',
            f'{18*"#"}',
            sep="\n",
        )
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
    t0 = time()
    accept_terms_button = 0

    while not accept_terms_button:
        try:
            accept_terms_button = cro.find_element_by_class_name("css-lolz04")
            accept_terms_button.click()
            return 1

        except:
            elapsed_time = time() - t0
            if elapsed_time > timeout:
                this_func = inspect.stack()[0][3]
                f"\n\n{9*'#'}\nTimeout...{this_func}\n{9*'#'}"
                return 0
            sleep(1)


def got_search_results(cro, timeout=30):
    t0 = time()
    search_results_msg = "empty"
    regex = re.compile(C.GOT_RESULTS)

    while not bool(re.match(regex, search_results_msg)):
        try:
            search_results_msg = cro.find_element_by_class_name("css-15u79n8").text
            results_found = search_results_msg.split(" ")[1]

        except:
            search_results_msg = cro.find_element_by_class_name("css-ujlbbb").text

            results_found = search_results_msg.split(" ")[1]

            # TIMEOUT!
        elapsed_time = time() - t0
        if elapsed_time > timeout:
            this_func = inspect.stack()[0][3]
            f"\n\n{18*'#'}\nTimeout...{this_func}\n{18*'#'}"
            return 0
        sleep(1)

    return results_found
