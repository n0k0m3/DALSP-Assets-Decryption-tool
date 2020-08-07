# Date A Live: Spirit Pledge Assets Decryption tool
Decrypt assets for the game (WIP)
## Notes
- This tool can only decrypt textassets (lua,json,etc.), visual/audio assets (mp3,mp4)
- Some PNGs can be decrypted to PVR encrypted (will need to decrypt later)  
- Most other visual assets (other PNGs, Live2D - due to encrypted PNG) cannot be decrypted for now
## Usage
```
python main.py -h

Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -i "DIR_IN", --input="DIR_IN"
                        Encrypted Data Directory
  -o "DIR_OUT", --output="DIR_OUT"
                        Decrypted Data Directory
  -v, --verbose         Print status messages to stdout
```