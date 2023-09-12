# The benevolent dictators - Benevolens

### Python Discord Code Jam 2023

![banner](doc/img/team-banner.png)

Benevolens is an automatic secret code translation tool!
It's main functionality consists on passing an image with a secret code somewhere on it, then benevolens will create a new image that contains the decoded text.

## Installation

### Virtual Enviroment
If you don't want to install anything into your base python installation you can follow the [enviroment creation instructions](https://github.com/ransomw/the-benevolent-dictators/blob/main/doc/template-readme.md#creating-the-environment) to create your own virtual enviroment.

### Tesseract
Our program uses [Tesseract](https://github.com/tesseract-ocr/tesseract) to read text from images. You'll need to install it separatelly from one of the following sources. IMPORTANT!! Especially if you are on Windows, keep note of the absolute path to the tesseract executable (`tesseract.exe`).
#### Windows
https://github.com/UB-Mannheim/tesseract/wiki#tesseract-installer-for-windows
#### Linux
In linux you can use a package manager to install tesseract:
for Ubuntu, install the package `tesseract-ocr`,
for FreeBSD install the package `tesseract`.

### Building Benevolens
You'll need to have `build` installed. If you are using a `venv` you need to make sure that it is activated now.

To install `build`:
`python -m pip install build`

Once you have `build` installed, make sure you are on the main `the-benevolent-dictators` directory and run the following command:
```
python -m build
```
You'll see a new `/dist` directory being created.

On Windows you need to:
```
python -m pip install .\dist\benevolent-0.0-py3-none-any.whl
```
Now that you have benevolens installed you should:
```
benevolens create-config
```
And paste the absolute path to your `tesseract.exe` (that you hopefully saved earlier) in the prompt that you are given.

On Linux you need to:
## TODO

Note: if you get any `tesseract not found` errors while trying to use the program, try to:
```
benevolens create-config
```
And paste the absolute path to your tesseract executable.


## Usage

### Help
```shell
python -m benevolent --help
```

### Basic usage
```shell
python -m benevolent xor-code test/images/acolchado.jpg test/images/sheet.jpg as_xor.jpg
```
