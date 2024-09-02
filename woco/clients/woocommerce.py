import logging
import woco.config as cfg

from woocommerce import API as wcapi

logger = logging.getLogger(__name__)

class WooCommerce:
    def __init__(self) -> None:
        self.wc = wcapi(
            url=cfg.SITE_URL,
            consumer_key=cfg.WOOCOMMERCE_CONSUMER_KEY,
            consumer_secret=cfg.WOOCOMMERCE_CONSUMER_SECRET,
            timeout=100,
        )

    def get_products(self, limit=20):
        try:
            products = self.wc\
                .get("products", params={"per_page": limit})\
                .json()

            return products
        except Exception as ex:
            logger.exception(f"Failed to get products. {ex}")
            raise ValueError(str(ex))

    def get_product(self, id: str):
        try:
            product = self.wc\
                .get(f"products/{id}")\
                .json()

            return product
        except Exception as ex:
            logger.exception(f"Failed to get product. {ex}")
            raise ValueError(str(ex))

    def add_products(self, payload: dict):
        try:
            product = self.wc.post('products', data=payload).json()
            return product
        except Exception as ex:
            logger.exception(f"Failed to add products. {ex}")
            raise ValueError(str(ex))
