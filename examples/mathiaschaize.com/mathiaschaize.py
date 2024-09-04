import os

from woco.shared.data import get_data_files, is_likely_json_file
from woco.shared.constants import STORE_PATH
from woco.shared.io import read_json_file

def main():
    # Get latest transactions
    root_dir = os.path.basename(STORE_PATH)
    data = get_data_files([root_dir], is_likely_json_file)
    data = sorted(data, reverse=True)[0]
    products = read_json_file(data)
    product_imgs = []
    for product in products:
        images = [image['name'] for image in product['images']]
        product_imgs.extend(images)

    print("\n".join(product_imgs))

if __name__ == "__main__":
    main()
