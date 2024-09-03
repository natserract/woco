# woco
Upload woocommerce product script for mathiaschaize.com

## Usage
```
usage: woco [-h] {run} ...

Woco command line interface.

positional arguments:
  {run}       Woco commands
    run       Starts Woco CLI

options:
  -h, --help  show this help message and exit
```

# Default. (Source: use cloudinary, fixed price)
woco run -c config.yml
woco run --config config.yml

# (Source: use local, define own price)
woco run -d data/jewellery_ring.json -c config.yml
woco run --data data/jewellery_ring.json --config config.yml
