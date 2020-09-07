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

Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -i "INPUT", --input="INPUT"
                        Encrypted Data Source (folder/file; if file, use -f)
  -o "OUTPUT", --output="OUTPUT"
                        Decrypted Data Destination (MUST BE A FOLDER)
  -f, --file            Single file decryption mode
  -v, --verbose         Print debug messages to stdout and debug.log
  -u, --unpack          Unpack PVR assets
  -k, --keepPVR         Keep PVR assets after unpack
  -w, --overwrite       Overwrite assets even if decrypted assets exist at
                        destination
  ```
  ## Example
  Directory decryption mode, overwrite, unpack PVR but not keeping file, log to debug.log
  ```
  python main.py -i example -o example_out -w -u -v
  ```
  Single file decryption mode, overwrite, unpack PVR and keeping file, log to debug.log
  ```
  python main.py -i example/icon-gift/531009.png -o example/icon-gift -w -u -v -k
  ```
