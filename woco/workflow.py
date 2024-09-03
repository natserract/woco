import os
import argparse

from pathlib import Path
from datetime import datetime
from woco.shared.constants import STORE_PATH
from woco.shared.data import get_data_files, is_config_file
from woco.shared.io import dump_obj_as_json_to_file, read_config_file
from woco.clients.cloudinary import Cloudinary
from woco.shared.utils import normalize_name

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
                #self._write_data_store_file(model['name'], assets)
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

    def _write_data_store_file(self, name: str, assets: list[dict]):
        dir = STORE_PATH
        timestamp = datetime.now().isoformat()
        file_name = f"{normalize_name(name)}_{timestamp}"
        file_path = Path(f"{dir}/{file_name}.json")

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
