# Date A Live: Spirit Pledge Assets Decryption tool

Decrypt assets for the game

## Requirements

- [Python 3.6 or 3.7](https://www.python.org/downloads/) (other versions are untested but minimum is Python 3+)
- pip modules `lz4-python`, `Pillow`, `tex2img`: `pip install -r requirements.txt`

## Notes

This tool can decrypt/unpack following assets automatically:

- Text assets (lua,json,etc.)
- Audio/video assets (mp3,mp4)
- PNGs assets (Live2D textures,Spine sprites, PVR textures)

## Usage

```
> python main.py -h

Date A Live: Spirit Pledge Assets Decryption tool

usage: main.py [-h] [-v] [-k] [-w] [-e] [-m MODE] INPUT OUTPUT

Decrypt all assets in source directory and save in destination directory

positional arguments:
  INPUT                 Encrypted Data Source (folder/file)
  OUTPUT                Decrypted Data Destination (MUST BE A FOLDER)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print debugging messages to debug.log

decryption options:
  Some useful decryption options.

  -k, --keepPVR         Keep PVR assets after unpack (Recommended for
                        debugging)
  -w, --overwrite       Overwrite assets even if decrypted assets exist at
                        destination

encryption options:
  Currently in testing. NOTE: For encryption mode PCM, you can explicitly
  set hex XOR value (4th byte of the original file) by "-m pcm,<xor_hex>" to
  produce identical result. However, this is not needed in the whole
  decryption scheme in the game

  -e, --encryption      Enable encryption mode
  -m MODE, --mode MODE  Encryption mode (ZIP,LZ4,PCM)
```

## Example

Directory decryption mode, overwrite, unpack PVR but not keeping file, log to debug.log

```
python main.py example example_out -w -v
```

Single file decryption mode, overwrite, unpack PVR and keeping file

```
python main.py example/icon-gift/531009.png example/icon-gift -w -k
```

Single file encryption, PCM mode with 0x4C as XOR variable (not specified means random) (Not in development)

```
python main.py example_dec/video/cap2.mp4 example_dec_enc -v -e -m pcm,4c
```

# Extras

<details>
  <summary> AWB download and extract scripts</summary>

Download external assets .awb from ext_assets (Android only). Supports downloading from EN and CN (default) region.

## Usage

```
usage: awb.py [-h] [-r REGION] [-t] OUTPUT

Download and extract external .awb assets

positional arguments:
  OUTPUT                Extracted Data Destination (MUST BE A FOLDER)

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        Choose the region of the assets (EN/CN), default: CN
  -t, --test            Test mode, only download 3 files.
```

## Example

Test download assets from EN server

```
python awb.py example -t -r EN
```

</details>
