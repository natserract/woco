import os
import argparse

from woco.shared.data import get_data_files, is_config_file
from woco.shared.io import read_config_file
from woco.clients.cloudinary import Cloudinary

class Workflow:
    def __init__(self) -> None:
        self._cloudinary = Cloudinary()

    def run_workflow(self, config_path: str):
        try:
            path = os.path.join(config_path)
            config = read_config_file(path)
            models = config['model']

            for model in models:
                assets = self._fetch_assets(model['image'])
                print(assets)
        except Exception as ex:
            raise ValueError(ex)
            sys.exit(1)

    def _fetch_assets(self, image: dict) -> list[dict]:
        assets = self._cloudinary.get_assets(
            dir=image['path'],
            sort_by=(image['sort']['name'], image['sort']['order_by']),
            max_results=image.get('max_results') or 2,
            excludes=image['excludes']
        )

        return assets
