# the benevolent dictators

### Python Discord Code Jam 2023

![banner](doc/img/team-banner.png)

##### install

```
python -m venv .venv
. ./.venv/bin/activate
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

install [tesseract](https://github.com/tesseract-ocr/tesseract)

for Ubuntu, install the package `tesseract-ocr`,
for FreeBSD install the package `tesseract`,
and for Windows

**todo**

for windows systems, it's necessary to give the path to tesseract
via a config file.  run

```
python -m benevolent print-config-path
```

to determine where to place this file, and put as its contents

```
[tesseract]
path=<path-on-your-system>
```

##### run

```shell
python -m benevolent --help
```

for instance

```shell
python -m benevolent xor-code test/images/acolchado.jpg test/images/sheet.jpg as_xor.jpg
```
