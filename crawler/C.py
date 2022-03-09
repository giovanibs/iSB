BINANCE_NFT_HOME = "https://www.binance.com/en/nft/home"
SELENIUM_DRIVERS_PATH = r"C:\SeleniumDrivers"
RESULT_DIV = "css-17xwdo2"
RESULT_DIV_SMALL_SCREEN = "css-9uhf7y" # small screen
GOT_RESULTS = r"Showing . results of NFT Items:" # regex
RESULTS_ORDER = {
    "Ending soon": "set_end_time%401",
    "Recently listed": "list_time%40-1",
    "Price low - high": "amount_sort%401",
    "Price high - low": "amount_sort%40-1",
    "Most favorited": "favorites%40-1",
}
ORDER_OPTIONS = {
    1: "Ending soon",
    2: "Recently listed",
    3: "Price low - high",
    4: "Price high - low",
    5: "Most favorited",
}
B_ELEMS = {
    "search_input": {
        "short_xpath": "//input",
        "css_finder": ".css-16fg16t:nth-child(2)",
        "xpath_relative_ID": "//div[@id='__APP']/div/div/header/div[2]/div/div/div/div/div/input",
    },
    "accept_terms": {"class": "css-lolz04"},
}

RESULT_INFOS_WITH_REMAINING_TIME = [
    "favorites",
    "clock_icon",
    "remaining_time",
    "title",
    "BSC",
    "price_or_bid",
    "value",
    "value_in_current_currency",
    "creator_label",
    "creator_name"
]

RESULT_INFOS_WO_REMAINING_TIME = [
    "favorites",
    "clock_icon",
    "remaining_time",
    "title",
    "BSC",
    "price_or_bid",
    "value",
    "value_in_current_currency",
    "creator_label",
    "creator_name"
]
