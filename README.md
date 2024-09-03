# Woco

Command line interface for uploading WooCommerce(WC) products in efficient way.

## Installation

First make sure your pip version is up to date:
```bash
pip3 install -U pip
```

To install Woco:
```bash
pip3 install woco # (not yet published, DON'T run this for a while)
```

## Development

### Managing Environments
```bash
pyenv install 3.11.9
pyenv local 3.11.9  # Activate Python 3.11.9 for the current project
```

*Note*: If you have trouble installing a specific version of python on your system it might be worth trying other supported versions.

**Create and activate a virtual environment**

```bash
pyenv exec python3 -m venv .venv
source .venv/bin/activate
```

### Building from source
To install dependencies and `woco` itself in editable mode execute

```bash
python setup.py install
make build-source
```

## Usage

|        Command           |                                                                  Effect                                                                  |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
|`woco run`                |Starts uploading your products.                                                                                                           |
|`woco -h`                 |Shows all available commands.                                                                                                             |

### woco run

To start uploading your products, run:

```bash
woco run
```

The following arguments can be used to configure your Woco:

```bash
usage: woco run [-h] [-v] [-vv] [--quiet] [--logging-config-file LOGGING_CONFIG_FILE] [-d DATA [DATA ...]] [-c CONFIG] [--disable-out-file] [-m {local,cloud}] {update,remove} ...

positional arguments:
  {update,remove}
    update              Update WooCommerce products
    remove              Remove WooCommerce products

options:
  -h, --help            show this help message and exit
  -d DATA [DATA ...], --data DATA [DATA ...]
                        Paths to the files or directories containing Woco data. (default: data)
  -c CONFIG, --config CONFIG
                        Path to config file (default: config.yml)
  --disable-out-file    Disable out files for data store output (default: False)
  -m {local,cloud}, --media {local,cloud}
                        Source for fetch media (e.g. local, cloud) (default: cloud)

Python Logging Options:
  You can control level of log messages printed. In addition to these arguments, a more fine grained configuration can be achieved with environment variables. See online documentation
  for more info.

  -v, --verbose         Be verbose. Sets logging level to INFO. (default: None)
  -vv, --debug          Print lots of debugging statements. Sets logging level to DEBUG. (default: None)
  --quiet               Be quiet! Sets logging level to WARNING. (default: None)
  --logging-config-file LOGGING_CONFIG_FILE
```

## Suggested Config

Example `config.yml` file:

```yaml
model:
  - name: "jewellery/ring"

    image:
      path: "mathiaschaize.com/upload/shop/ring"
      sort:
        name: "uploaded_at"
        order_by: "asc"
      max_results: 8

    product:
      type: "simple"
      price:
        euro:
          value: 75
          default: true
          currency: EURO
        idr:
          value: 1200000
          currency: IDR

      stock_status: "instock"
      categories:
        - jewellery:
            id: 27
            name: "Jewellery"
            slug: "jewellery"

        - ring:
            id: 31
            name: "Ring"
            slug: "ring"
```
