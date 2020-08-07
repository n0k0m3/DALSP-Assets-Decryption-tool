# Date A Live: Spirit Pledge Assets Decryption tool
Decrypt assets for the game (WIP)
## Notes
- This tool can only decrypt textassets for now (lua,json,etc.)  
- Some PNGs can be decrypted to PVR encrypted (will need to decrypt later)  
- Most other visual assets (movies,cg,l2d) cannot be decrypted for now
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