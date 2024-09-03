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

### Default. (Source: use cloudinary, fixed price)
woco run -c config.yml
woco run --config config.yml

### (Source: use local, define own price)
woco run -d data/jewellery_ring.json -c config.yml -m local
woco run --data data/jewellery_ring.json --config config.yml --model local

### (Update)
woco update -k jewellery_ring_2024-09-03T20:03:49.225646

### (Delete)
woco remove -k jewellery_ring_2024-09-03T12:34:56.789123
woco remove --key jewellery_ring_2024-09-03T12:34:56.789123
