# binance NFT market crawler
import C
import os
import sys
import inspect
from time import sleep, time
from selenium.webdriver import Firefox
from methods import *

os.environ["PATH"] += os.pathsep + C.SELENIUM_DRIVERS_PATH
print('Opening broswer...')
cro = Firefox()

print('Getting binance nft webpage...')
cro.get(C.BINANCE_NFT_HOME)

lets_rock = accept_terms(cro, timeout=30)

sleep(3)

if lets_rock:

    while True:
        search_term = input("\nTerms to search for: -> ")

        search_has_no_results = not search(cro, search_term)

        if search_has_no_results:
            command = input(
                "No results were found! Wanna search something else? [y/n] -> "
            )
            if command.lower().strip() == "n":
                sys.exit()
            else:
                continue  # prompt search term again

        ### EVERYTHING HAS LOADED *fingers crossed*

        while True:
            results_list = read_results(cro)
            
            if not results_list:
                print("Algo deu errado em results_list")
                break
            
            print_results(results_list)

            print("Sorting options:\n")
            for option, order_by in C.ORDER_OPTIONS.items():
                print(f"\t{option}: {order_by}")

            order_option = input("\nSorting option (or exit): -> ")

            if order_option.lower().strip() == "exit":
                sys.exit()

            if not order_results(cro, order_option * 1):
                print("Algo deu errado...")

sys.exit()

# maximized window: getElementsByClassName("css-43igg3")[0]
# small window: getElementsByClassName("css-1p3lb33")[0]


# <button class=" css-lolz04" data-bn-type="button">
# textContent: "Accept"
# innerHTML: "Accept"
# innerText: "Accept"
# d.getElementsByClassName("css-lolz04")[0].click()
