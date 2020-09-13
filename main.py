import os
from optparse import OptionParser

from dalsp_crypt import dalsp_decrypt
from dalsp_crypt import dalsp_encrypt


def main():
    print("Date A Live: Spirit Pledge Assets Decryption tool\n")
    print("Decrypt all assets in source directory and save in destination directory\n")
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_path",
                      help="Encrypted Data Source (folder/file)", metavar="\"INPUT\"")
    parser.add_option("-o", "--output", dest="output_path",
                      help="Decrypted Data Destination (MUST BE A FOLDER)", metavar="\"OUTPUT\"")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print debug messages to debug.log")
    parser.add_option("-u", "--unpack",
                      action="store_true", dest="unpackPVR", default=False,
                      help="Unpack PVR assets")
    parser.add_option("-k", "--keepPVR",
                      action="store_true", dest="keepPVR", default=False,
                      help="Keep PVR assets after unpack")
    parser.add_option("-w", "--overwrite",
                      action="store_true", dest="overwrite", default=False,
                      help="Overwrite assets even if decrypted assets exist at destination")
    parser.add_option("-e", "--encryption", action="store_true", dest="encryption", default=False,
                      help="Enable encryption mode")
    parser.add_option("-em", "--mode", dest="encrypt_mode",
                      help="Encryption mode (ZIP,LZ4,PCM)", metavar="\"MODE\"")


    (options, args) = parser.parse_args()

    if options.input_path is None or options.output_path is None:
        print()
        print("No input or output path specified. Run \"python main.py -h\" for more details")
        print()
        return
    if not options.encryption:
        decrypt = dalsp_decrypt.DateALive_decryption(options)
        if os.path.isfile(options.input_path):
            decrypt.crypt_single_file()
        else:
            decrypt.crypt_folder()
        plistout = os.path.join(options.output_path, "info.plist")
        if os.path.exists(plistout):
            os.remove(plistout)
    else:
        encrypt = dalsp_encrypt.DateALive_encryption(options)
        if os.path.isfile(options.input_path):
            encrypt.crypt_single_file()
        else:
            encrypt.crypt_folder()


if __name__ == "__main__":
    main()
