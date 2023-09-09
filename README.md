# The benevolent dictators

### Python Discord Code Jam 2023

![banner](doc/img/team-banner.png)

## Installation

### Linux
```
python -m venv .venv
. ./.venv/bin/activate
pip install -r dev-requirements.txt
pip install -r requirements.txt
```



Install [tesseract](https://github.com/tesseract-ocr/tesseract)

for Ubuntu, install the package `tesseract-ocr`,
for FreeBSD install the package `tesseract`,

### Windows
```
python -m venv .venv
. ./.venv/Scripts/activate
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

On Windows it's necessary to provide tesseract a config file. Use the following command to get the config file path
<br>[Tesseract Direct Download Link](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe)
```
python -m benevolent print-config-path
```

Paste the following file content into the config file.
The default tesseract.exe path is ``C:\Program Files\Tesseract-OCR\tesseract.exe``

```
[tesseract]
path=<path-on-your-system>
```

## Usage

### Help
```shell
python -m benevolent --help
```

### Basic usage
```shell
python -m benevolent xor-code test/images/acolchado.jpg test/images/sheet.jpg as_xor.jpg
```
## Build

```shell
python3 -m build
```

then one can install the `.whl` file in `dist/` with `pip` _in a different `venv` than for development_

the command (executable) made available by this install is `benevolens`