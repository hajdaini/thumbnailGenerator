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
thumbnailGenerator.py [-h] [--text TEXT] [--size SIZE]
                             [--offsetY OFFSETY] [--file FILE]
```

Arguments Description
--------------

| name          | type   | description                                     | mandatory |
|---------------|--------|-------------------------------------------------|-----------|
| `text`        | string | text to display in your image                   |   false   |
| `size`        | int    | size of the text that will be display           |   false   |
| `offsetY`     | int    | Offset in y position of the text                |   false   |
| `file`        | string | Select text line by line from a file            |   false   |


