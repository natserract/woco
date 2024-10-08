import os
import argparse
import re
import logging
import time

from pathlib import Path
from datetime import datetime
from typing import Literal, Optional, Text, Any, Union
from woco.shared.constants import STORE_PATH
from woco.shared.data import get_data_files, is_config_file
from woco.shared.io import dump_obj_as_json_to_file, read_config_file, read_json_file
from woco.shared.utils import normalize_name
from woco.clients.media_storage.base import MediaStorage
from woco.clients.media_storage.cloudinary import Cloudinary
from woco.clients.woocommerce import WooCommerce

logger = logging.getLogger(__name__)

OPTIONS = Literal[
    'disable_out_file', # bool
    'media_source', # local, cloud
]

class Workflow:
    def __init__(
        self,
        media_storage: Optional['MediaStorage'] = None,
        payload_builder: Optional['PayloadBuilder'] = None,
        options: dict[OPTIONS, Any] = {}
    ) -> None:
        self._woocommerce = WooCommerce()

        default_opts: dict[OPTIONS, Any] = {
            'disable_out_file': False,
            'media_source': 'cloud',
        }
        self._options: dict[OPTIONS, Any] = {
            **default_opts,
            **options, # let overrides default options
        }
        if media_storage is not None:
            self._media_storage = media_storage
        else:
            self._media_storage = Cloudinary()

        if payload_builder is not None:
            self._payload_builder = payload_builder
        else:
            self._payload_builder = DefaultPayloadBuilder()

    @property
    def is_local_source(self):
        return self._options['media_source'] == 'local'

    @property
    def is_cloud_source(self):
        return self._options['media_source'] == 'cloud'

    def run_workflow(
        self, config_path: str
    ):
        try:
            path = os.path.join(config_path)
            config = read_config_file(path)
            models = config['model']

            # Option: Media storage source
            if self.is_cloud_source:
                for model in models:
                    logger.info(f"Processing: {model['name']}")

                    product_model = model['product']
                    image_model = model['image']
                    images = self._fetch_assets(image_model)
                    payloads = []
                    for image in images:
                        payload = self._payload_builder.build_payload(
                            product_model=product_model,
                            image_model=image_model,
                            image_data=image
                        )

                        # Request
                        logger.info(f"Create product: {payload['name']}")
                        start_time = time.time()
                        product = self._woocommerce.add_products(payload)
                        end_time = time.time()
                        logger.info(f"Successfully add {product['id']}, {product['name']}. Total time: {end_time - start_time}")

                        payloads.append({
                            **payload,
                            'id': product['id'],
                            'image_ids': [img['id'] for img in product['images']]
                        })

                    if not self._options['disable_out_file']:
                        self._write_data_store_file(model['name'], payloads)

                    logger.info(f"Done: {model['name']}")

            elif self.is_local_source:
                raise NotImplementedError
            else:
                raise NotImplementedError
                sys.exit(1)

        except Exception as ex:
            raise ValueError(ex)
            sys.exit(1)

    def run_remove_workflow(
         self, config_path: str, key_path: str
    ):
        try:
            path = os.path.join(config_path)
            config = read_config_file(path)
            models = config['model']

            # Read key path .json
            dir = STORE_PATH
            data = read_json_file(f"{dir}/{key_path}.json")
            for item in data:
                product_id = item['id']
                product_image_ids = item['image_ids']

                logger.info(f"Delete product: {product_id}")
                start_time = time.time()
                self._woocommerce.remove_product(product_id)
                end_time = time.time()
                logger.info(f"Successfully remove {product_id}. Total time: {end_time - start_time}")

        except Exception as ex:
            raise ValueError(ex)
            sys.exit(1)

    def run_update_workflow(
          self, config_path: str, key_path: str
     ):
         raise NotImplementedError

    def _fetch_assets(self, image: dict) -> list[dict]:
        logger.info('Fetch images from media storage')
        assets = self._media_storage.get_assets(
            dir=image['path'],
            sort_by=(
                image['sort']['name'],
                image['sort']['order_by'],
            ),
            max_results=image.get('max_results') or 2,
            excludes=image.get('excludes') or []
        )

        return assets

    def _write_data_store_file(self, name: str, assets: Union[list[dict], dict]):
        dir = STORE_PATH
        timestamp = datetime.now().isoformat()
        file_name = f"{normalize_name(name)}_{timestamp}"
        file_path = Path(f"{dir}/{file_name}.json")

        logger.info(f"Store out file to {dir}/{file_name}.json")
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
                file_path = Path(f"{dir}/{file_name}.json")
                dump_obj_as_json_to_file(file_path, assets)
            except Exception as ex:
                raise IOError(ex)
                sys.exit(1)
        else:
            dump_obj_as_json_to_file(file_path, assets)


class PayloadBuilder:
    @classmethod
    def name(cls) -> Text:
        return cls.__name__

    def build_payload(
        self, product_model: dict, image_model: dict, image_data: dict, **kwargs: Any
    ):
        raise NotImplementedError(
            "Payload builder needs to implement a build payload for create structured payload based on your own."
        )

class DefaultPayloadBuilder(PayloadBuilder):
    """
    Our structured payload for https://mathiaschaize.com
    """
    @classmethod
    def name(cls) -> Text:
        return "default_payload_builder"

    def build_payload(
        self, product_model: dict, image_model: dict, image_data: dict, **kwargs: Any
    ):
        logger.info(f'Build structured payload...')
        payload = {
            "type": product_model['type'],
            "categories": [],
            "stock_status": product_model['stock_status'],
            "images": [],
            "meta_data": [
              { "key": "_wcml_custom_prices_status", "value": "1" },
            ]
        }

        # Set product name
        match = re.match(r'([A-Z]+)(\d+)', image_data['filename'])
        if match:
            product_name = f"{match.group(1)}-{match.group(2)}"
            payload['name'] = product_name
        else:
            payload['name'] = image_data['filename']

        # Set product description
        payload['description'] = payload['name']

        # Set product featured image
        payload['images'] = [
            {
                "src": f"https://res.cloudinary.com/dmg89x9bd/images/f_auto,q_auto/v1725243298/{image_model['path']}/{image_data['filename']}/{image_data['filename']}.{image_data['format']}?_i=AA",
                "name": image_data['filename'],
                "alt": ""
            }
        ]

        # Set product price + multi currencies
        price: dict = product_model['price']
        price_key = list(price.keys())[0]
        regular_price: dict = {
            **list(price.values())[0],
        }
        for key, p in price.items():
            if p.get('default') == True:
                regular_price = p
                price_key = key

        payload['price'] = str(regular_price['value'])
        payload['regular_price'] = str(regular_price['value'])
        payload['price_html'] = \
            f"<span class=\"woocommerce-Price-amount amount\"><bdi><span class=\"woocommerce-Price-currencySymbol\">&{str(regular_price['currency']).lower()};</span>{regular_price['value']}</bdi></span>",

        # Set product metadata
        custom_prices: list[dict] = [p for key, p in price.items() if key != price_key] # other prices
        for pr in custom_prices:
            value = int(pr['value'])
            currency = str(pr['currency']).upper()

            payload['meta_data'].append(
                { "key": f"_sale_price_dates_to_{currency}", "value": "" },
            )
            payload['meta_data'].append(
                { "key": f"_sale_price_dates_from_{currency}", "value": "" },
            )
            payload['meta_data'].append(
                { "key": f"_sale_price_{currency}", "value": "" },
            )
            payload['meta_data'].append(
                { "key": f"_regular_price_{currency}", "value": str(value) },
            )
            payload['meta_data'].append(
                { "key": f"_wcml_schedule_{currency}", "value": "0" },
            )
            payload['meta_data'].append(
                { "key": f"_price_{currency}", "value": str(value) },
            )

        # Set product categories
        # Set cloudinary metadata
        cloudinary_tf_term_payload = {
            "key": "cloudinary_transformations_terms",
            "value": []
        }
        for categories in product_model['categories']:
            category = list(dict(categories).values())[0]
            payload['categories'].append(category)

            cloudinary_tf_term_payload['value'].append(
                f"category:{category['id']}"
            )

        payload['meta_data'].append(cloudinary_tf_term_payload)
        payload['meta_data'].append(
            { "key": "_cloudinary_featured_overwrite", "value": "" }
        )

        return payload
