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
```
python3 -m pip install .\dist\benevolent-0.0-py3-none-any.whl
```
and ensure `tesseract` is on your `PATH` environment variable so that `which tesseract` should print the path.


Note: if you get any `tesseract not found` errors while trying to use the program, try to:
```
benevolens create-config
```
And paste the absolute path to your tesseract executable.


## Usage

### Some considerations about image recognition
Tesseract doesn't work perfectly! Especially not for handwritten text. You can do the following to help our tool better recognize the text you write:
- Use black ink or a black marker on a white paper.
- When you take the picture, try to get the text is as aligned as possible.
- Try to get the same lighting in all the text.
- Try to have a nice handwriting.
- Absolutelly no cursive.

These are a lot of considerations! We do some image manipulation on the background to help tesseract better recognize your images, but it may still misinterpret a couple of letters.

Later you'll find a couple of commands you can also use to make tesseract's life easier: `box-write` which directly writes some text to the image (bypassing basically all considerations) and `benevolens-segments` which lets you specify which segment of
the image your text is located in.
- If you want to just use `benevolens` instead of `benevolens-segments`, then try to take a photo that contains only the paper with writing in it.

### NOTE:
We messed up a path and the commands will only work if your are in the `the-benevolent-dictators` directory when launching them. Sorry we didn't realize before!

If you really wanted to use our commands from a specific directory (maybe it makes it easier if you have a lot of images there), then you can copy the `fonts` directory and paste it in the directory you want to call `benevolens` from.

### Commands
#### benevolens
Our main functionality!

`benevolens` takes in an image that contains some encoded text and outputs and image with that section translated.

To use it you have two options:

(Yes, you have to write benevolens twice.)

(If the text was encoded with a cipher file:)
```
benevolens benevolens [path_to_the_image_you_want_to_translate] --cipher-path [path_to_the_cipher_file] [path_to_save_output_image]
```
(If the text was encoded with a seed:)
```
benevolens benevolens [path_to_the_image_you_want_to_translate] --cipher-seed [seed used to encode the text] [path_to_save_output_image]
```
#### benevolens-segments
Works like benevolens but lets you specify which segment of the image the text is located in (sorry, it's called segments but you can only do one at a time!). This is useful if you have an image with a lot of stuff in it and the
paper with your text is located in only one part of the image.

Just like with `benevolens` you have to specify either a `--cipher-path` or a `--cipher-seed`:
```
benevolens benevolens [path_to_the_image_you_want_to_translate] --cipher-seed [seed used to encode the text] x1 y1 x2 y2 [path_to_save_output_image]
```
The values of `x1 y1 x2 y2` can be obtained as follows:
```
Your image:
    ___________________________________________
    |                                         |
    | (x1, y1) *_____________                 |
    |          |             |                |
    |          | coded text  |                |
    |          |             |                |
    |          ‾‾‾‾‾‾‾‾‾‾‾‾‾‾*(x2, y2)        |
    |                                         |
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

#### xor-code

This commands lets you input two images and generates a third image which is the result of running a bitwise xor between both inputs.

What's interesting about this? That you can xor-code the resulting image alongside one of the original images to obtain the other original image:
```
(example)
[image1] xor-code [image2] = [xor1-2]
[image1] xor-code [xor1-2] = [image2]
[image2] xor-code [xor1-2] = [image1]
```
In this way, you can use the resulting xor image alongside one of the original images as a "code" to obtain the other.

To use this command call:

`benevolens xor-code [path_to_image1] [path_to_image2] [path_to_save_output_image]`

NOTE: We've tested this command with `.jpg`, `.png` and `.bmp` images. Using the first two formats may result in artifacts appearing in your image after you try to recreate the original. You can use `.bmp` if you don'r want any artifacts.


#### generate-cipher

Generate cipher allows you to create a cipher file. This is a simple text file with the code (keep it secret!) to encode and decode messages using a substitution cipher. This could be useful if you tried to use seeds to encode and decode but encounter errors
between machines (although we ran unit tests and it did not happen happen).

To use this command call:
```
benevolens generate-cipher [path_to_save_the_cipher]
```
(Optionally)
```
benevolens generate-cipher [path_to_save_the_cipher] --cipher-seed [a seed to use to generate the cipher (can be any string)]
```

#### encode-with-cipher

This command lets you generate your secret messages with a given code.

NOTE: Please use only lowercase characters for your text!

You can use either of these options:

(If you have a cipher file that you want to use)
```
benevolens encode-with-cipher [a string of text you want to encode] --cipher-path [path_to_your_cipher_file]
```

(If you want to use a seed instead)
```
benevolens encode-with-cipher [a string of text you want to encode] --cipher-seed [a seed to use to encode (can be any string)]
```
Now that you have some encoded text you can go and write it in some paper and then take a photo!

You can also use `decode-with-cipher`, which works exactl like `encode-with-cipher` but in reverse. This is just a boring command line decoding, you should just use `benevolens` or `benevolens-segments` which actually do interesting things using images.
But the command is there if you need it for anything.

#### box-write

This command allows you to write some text inside an image. If you don't trust your handwriting, you can use this to write your encoded texts and it'll make it easier for `benevolens` to recognize the text.

To use it:
```
benevolens box-write [path_to_the_image_you_want_to_write] [string of text you want to write] --size [size for the text (a number)] -x [left coordinate of the text box] -y [top coordinate of the text box] [path_to_save_the_written_image_to]
```
