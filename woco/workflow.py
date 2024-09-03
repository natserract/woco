import os
import argparse

from woco.shared.data import get_data_files, is_config_file
from woco.shared.io import read_config_file

class Workflow:
    def run_workflow(self, config_path: str):
        try:
            # read config
            path = os.path.join(config_path)
            configs = read_config_file(path)
            print('read_yml_files', configs)
        except Exception as ex:
            raise ValueError(ex)
            sys.exit(1)
