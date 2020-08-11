# Date A Live: Spirit Pledge Assets Decryption tool
Decrypt assets for the game (WIP)
## Requirements
- [Python 3+](https://www.python.org/downloads/)
- [TexturePacker](https://www.codeandweb.com/texturepacker/download) (unpack PVR files) [added to PATH](https://github.com/n0k0m3/DALSP-Assets-Decryption-tool/wiki/Add-TexturePacker-to-PATH)
## Notes
- This tool can decrypt textassets (lua,json,etc.), audio/video assets (mp3,mp4)
- Some PNGs can be decrypted to PVR (will need to unpack with `TexturePacker`)  
- Most other visual assets (other PNGs, Live2D - due to encrypted PNG) cannot be decrypted for now
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
  -v, --verbose         Print debug messages to stdout
  -u, --unpack          Unpack PVR assets
  -k, --keepPVR         Keep PVR assets after unpack
  -w, --overwrite       Overwrite assets even if decrypted assets exist at
                        destination
  -d, --debug           Write debug info in stdout to file
  ```