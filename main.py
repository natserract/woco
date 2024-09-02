import logging
import logging.config
import config as cfg

from typing import List
from clients.cloudinary import Cloudinary
from clients.woocommerce import WooCommerce

log = logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    #cloudinary = Cloudinary()

    """
    # Has been uploaded
    excludes = [
        'RG20-S17B12-P1010277',
        'RG041-S15B28-P1010402',
        'RG023-S17B12-P1010281',
        'RG035-S40B20-P1010396',
        'RG018-S20B15-P1010274',
        'RG042-S29B18-P1010403'
    ]
    print(cloudinary.get_assets_shop('ring', excludes))
    """

    wc = WooCommerce()
    print(wc.get_products(limit=2))
