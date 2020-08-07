# Date A Live: Spirit Pledge Assets Decryption tool
Decrypt assets for the game (WIP)
## Notes
- This tool can only decrypt textassets (lua,json,etc.), visual/audio assets (mp3,mp4)
- Some PNGs can be decrypted to PVR encrypted (will need to decrypt later)  
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
  -v, --verbose         Print status messages to stdout
```