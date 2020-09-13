# Date A Live: Spirit Pledge Assets Decryption tool

Decrypt assets for the game

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- pip modules `lz4-python` and `Pillow`: `pip install -r requirements.txt`
- [TexturePacker](https://www.codeandweb.com/texturepacker/download) (unpack PVR files) [added to PATH](https://github.com/n0k0m3/DALSP-Assets-Decryption-tool/wiki/Add-TexturePacker-to-PATH)

## Notes

- This tool can decrypt textassets (lua,json,etc.), audio/video assets (mp3,mp4), some PNGs assets (Live2D textures)
- Other PNGs can be decrypted to PVR (will need to unpack with `TexturePacker`)
- <details>
  <summary>About TexturePacker Trial</summary>

  If you cannot afford TexturePacker, you can search Google for version 4.9.0 or older, these versions don't block Pro features after trial expired (you may find cracks of these versions as well).

</details>

## Usage

```
> python main.py -h

Date A Live: Spirit Pledge Assets Decryption tool

Decrypt all assets in source directory and save in destination directory

Usage: main.py -i INPUT -o OUTPUT [options]

Options:
  -h, --help            show this help message and exit
  -i "INPUT", --input="INPUT"
                        Encrypted Data Source (folder/file)
  -o "OUTPUT", --output="OUTPUT"
                        Decrypted Data Destination (MUST BE A FOLDER)
  -v, --verbose         Print debugging messages to debug.log

  Decryption Options:
    Some useful decryption options.

    -u, --unpack        Unpack PVR assets (Recommended)
    -k, --keepPVR       Keep PVR assets after unpack (Recommended for
                        debugging)
    -w, --overwrite     Overwrite assets even if decrypted assets exist at
                        destination

  Encryption Options:
    Currently in testing. NOTE: For encryption mode PCM, you can
    explicitly set hex XOR value (4th byte of the original file) by "-m
    pcm,<xor_hex>" to produce identical result. However, this is not
    needed in the whole decryption scheme in the game

    -e, --encryption    Enable encryption mode
    -m "MODE", --mode="MODE"
                        Encryption mode (ZIP,LZ4,PCM), case-insensitive
```

## Example

Directory decryption mode, overwrite, unpack PVR but not keeping file, log to debug.log

```
python main.py -i example -o example_out -w -u -v
```

Single file decryption mode, overwrite, unpack PVR and keeping file

```
python main.py -i example/icon-gift/531009.png -o example/icon-gift -w -u -k
```

Single file encryption, PCM mode with 0x4C as XOR variable (not specified means random)

```
python main.py -i python main.py -i example_dec/video/cap2.mp4 -o example_dec_enc -v -e -m pcm,4c
```
