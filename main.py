import os
from optparse import OptionParser, OptionGroup

from dalsp_crypt import dalsp_decrypt
from dalsp_crypt import dalsp_encrypt


def main():
    print("Date A Live: Spirit Pledge Assets Decryption tool\n")
    print("Decrypt all assets in source directory and save in destination directory\n")
    usage = "usage: %prog -i INPUT -o OUTPUT [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--input", dest="input_path",
                      help="Encrypted Data Source (folder/file)", metavar="\"INPUT\"")
    parser.add_option("-o", "--output", dest="output_path",
                      help="Decrypted Data Destination (MUST BE A FOLDER)", metavar="\"OUTPUT\"")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print debugging messages to debug.log")
    decryption = OptionGroup(parser, "Decryption Options",
                             "Some useful decryption options.")
    decryption.add_option("-u", "--unpack",
                          action="store_true", dest="unpackPVR", default=False,
                          help="Unpack PVR assets (Recommended)")
    decryption.add_option("-k", "--keepPVR",
                          action="store_true", dest="keepPVR", default=False,
                          help="Keep PVR assets after unpack (Recommended for debugging)")
    decryption.add_option("-w", "--overwrite",
                          action="store_true", dest="overwrite", default=False,
                          help="Overwrite assets even if decrypted assets exist at destination")
    parser.add_option_group(decryption)

    encryption = OptionGroup(parser, "Encryption Options",
                             "Currently in testing.\nNOTE: For encryption mode PCM, you can explicitly set hex XOR value (4th byte of the original file) by \"-m pcm,<xor_hex>\" to produce identical result.\nHowever, this is not needed in the whole decryption scheme in the game")
    encryption.add_option("-e", "--encryption", action="store_true", dest="encryption", default=False,
                          help="Enable encryption mode")
    encryption.add_option("-m", "--mode", dest="encrypt_mode",
                          help="Encryption mode (ZIP,LZ4,PCM), case-insensitive", metavar="\"MODE\"")
    parser.add_option_group(encryption)

    (options, args) = parser.parse_args()

    if options.input_path is None or options.output_path is None:
        print()
        print(
            "No input or output path specified. Run \"python main.py -h\" for more details")
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
        if options.encrypt_mode is not None:
            encrypt = dalsp_encrypt.DateALive_encryption(options)
            if os.path.isfile(options.input_path):
                encrypt.crypt_single_file()
            else:
                encrypt.crypt_folder()
        else:
            print(
                "Need to use \"-m\" with specified encryption modes: ZIP,LZ4 or PCM. Run \"python main.py -h\" for more details")
            return


if __name__ == "__main__":
    main()
