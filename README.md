# License Plate Removal

This is a lightly customised fork of [JPLeoRX/license-plate-removal](https://github.com/JPLeoRX/license-plate-removal), which uses OpenCV and Pillow to detect and obfuscate vehicle number plates.

**Usage:**

```
> ./main.py
Usage: main.py [OPTIONS]

  Obfuscate the number plate in the given image.

Options:
  -s, --source PATH       Source image path.  [required]
  -d, --destination PATH  Destination image path. Default is
                          <source>_obfuscated.<ext>
  -f, --force             Overwrite the destination file if it exists.
  -h, --help              Show this message and exit.
```

## Attribution

Thanks to [JPLeoRX](https://github.com/JPLeoRX) for their hard work on this! 

They wrote a [great tutorial](https://medium.com/@leo.ertuna/license-plate-removal-with-opencv-6649a3ac54e2) to go along with their [original source code](https://github.com/JPLeoRX/license-plate-removal).

They also wrote a cool blog post a couple of years later on the topic of more in-depth license plate detection. Worth a read [here](https://tekleo.net/blog/jump-start-in-object-detection-with-detectron2-(license-plate-detection))!
