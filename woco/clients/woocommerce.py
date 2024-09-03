import logging
from woco.config import (
    SITE_URL,
    WOOCOMMERCE_CONSUMER_KEY,
    WOOCOMMERCE_CONSUMER_SECRET
)
from woocommerce import API as wcapi

logger = logging.getLogger(__name__)

class WooCommerce:
    def __init__(self) -> None:
        self.wc = wcapi(
            url=SITE_URL,
            consumer_key=WOOCOMMERCE_CONSUMER_KEY,
            consumer_secret=WOOCOMMERCE_CONSUMER_SECRET,
            timeout=100,
        )

    def get_products(self, limit=20):
        try:
            products = self.wc\
                .get("products", params={"per_page": limit})
            products.raise_for_status()
            return products.json()
        except Exception as ex:
            logger.exception(f"Failed to get products. {ex}")
            raise ValueError(str(ex))

    def get_product(self, id: str):
        try:
            product = self.wc\
                .get(f"products/{id}")
            product.raise_for_status()
            return product.json()
        except Exception as ex:
            logger.exception(f"Failed to get product. {ex}")
            raise ValueError(str(ex))

    def add_products(self, payload: dict):
        try:
            product = self.wc.post('products', data=payload)
            product.raise_for_status()
            return product.json()
        except Exception as ex:
            logger.exception(f"Failed to add products. {ex}")
            raise ValueError(str(ex))

    def remove_product(self, id: str):
        try:
            deleted_product = self.wc.delete(f'products/{id}', params={"force": True})
            deleted_product.raise_for_status()
            return deleted_product.status_code
        except Exception as ex:
            logger.exception(f"Failed to remove product. {ex}")
            raise ValueError(str(ex))
