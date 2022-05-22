#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Get price of an item on bestbuy.com website using only SKU.

Using GET method get a json of the item and extract the price.
"""

__author__ = "Martin Pucovski"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Martin Pucovski"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Martin Pucovski"
__email__ = "martin@pucov.ski"
__status__ = "Production"

import configparser
import datetime
import logging
import sys
import json
import requests
from requests.structures import CaseInsensitiveDict

# get the SKU as parameter
item_id = sys.argv[1]

# Create and configure logger
current_day = datetime.datetime.now().strftime("%Y%m%d")

logging.basicConfig(filename=f"logs\{current_day}_log.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger
logger.setLevel(logging.INFO)

logger.info("####################")
logger.info("Script started")

# read config.ini file
logger.info("Reading config")
config = configparser.ConfigParser()
config.read('config\config.ini')
config_default = config['DEFAULT']


def get_price(sku_id: str) -> dict:
    """Get data for item using web request

    :param sku_id: code of the item
    :type sku_id: str

    :raises Exception: if error getting data from url

    :rtype: dict
    :return: json document with all info about item
    """
    # build the URL
    bestbuy_url = f'https://www.bestbuy.com/pricing/v1/price/item?allFinanceOffers=true&catalog=bby&context=offer-list&salesChannel=LargeView&skuId={sku_id}'

    # set header agent
    request_headers = CaseInsensitiveDict()
    request_headers["accept-language"] = "en-US,en;q=0.9"
    request_headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    request_headers["x-client-id"] = "lib-price-browser"

    # get response
    bestbuy_request = requests.get(bestbuy_url, headers=request_headers)

    # return response
    if bestbuy_request.status_code == 200:
        json_file = json.loads(bestbuy_request.content)
        return json_file
    
    raise Exception(f'Status code: {bestbuy_request.status_code}. Reason: {bestbuy_request.reason}')


def main():
    """
    Call function, print the price
    """

    request_response = get_price(item_id)
    print(f'Regular price: {request_response["regularPrice"]}')
    print(f'Current price: {request_response["currentPrice"]}')


if __name__ == "__main__":
    main()


logger.info("Script ended")
logger.info("####################")
