thumbnailGenerator
=========

This script generate automatic thumbnails for my blog [https://devopssec.fr/](https://devopssec.fr/)

Requirements
------------

- Linux os
- Install Pillow 
  ```shell
  sudo apt install python3-pil
  ```
- Install python packages from the file `requirements.txt` :
  ```shell
  sudo pip3 install -r requirements.txt
  ```

Usage
--------------

```shell
thumbnailGenerator.py [-h] [--text "You text here" ] [--size 90]
                             [--offsetY -200 ] [--file "/home/hajdaini/thumbnailGenerator/list.txt" ]
```

Arguments Description
--------------

| name                | type   | description                                     | mandatory |
|---------------------|--------|-------------------------------------------------|-----------|
| `--text` or `-t`    | string | text to display in your image                   |   false   |
| `--size` or `-s`    | int    | size of the text that will be display           |   false   |
| `--offsetY` or `-y` | int    | Offset in y position of the text                |   false   |
| `--file` or `-f`    | string | Select text line by line from a file            |   false   |


> You can also display a custom text in your image from the variable `textList` and save the image under another name from the variable   `textSave` (which will be slugify automatically) , in this case do not specify the `-f` or `-t` option


