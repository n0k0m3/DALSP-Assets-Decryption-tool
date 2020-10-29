import os
from argparse import ArgumentParser

from dalsp_crypt import dalsp_decrypt
from dalsp_crypt import dalsp_encrypt


def main():
    print("Date A Live: Spirit Pledge Assets Decryption tool\n")
    parser = ArgumentParser(description='Decrypt all assets in source directory and save in destination directory')
    parser.add_argument(dest="input_path",
                        help="Encrypted Data Source (folder/file)", metavar="INPUT")
    parser.add_argument(dest="output_path",
                        help="Decrypted Data Destination (MUST BE A FOLDER)", metavar="OUTPUT")
    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", default=False,
                        help="Print debugging messages to debug.log")
    decryption = parser.add_argument_group(title="decryption options",
                                           description="Some useful decryption options.")
    decryption.add_argument("-k", "--keepPVR",
                            action="store_true", dest="keepPVR", default=False,
                            help="Keep PVR assets after unpack (Recommended for debugging)")
    decryption.add_argument("-w", "--overwrite",
                            action="store_true", dest="overwrite", default=False,
                            help="Overwrite assets even if decrypted assets exist at destination")

    encryption = parser.add_argument_group(title="encryption options",
                                           description="Currently in testing.\nNOTE: For encryption mode PCM, you can "
                                                       "explicitly set hex XOR value (4th byte of the original file) "
                                                       "by \"-m pcm,<xor_hex>\" to produce identical "
                                                       "result.\nHowever, this is not needed in the whole decryption "
                                                       "scheme in the game")
    encryption.add_argument("-e", "--encryption", action="store_true", dest="encryption", default=False,
                            help="Enable encryption mode")
    encryption.add_argument("-m", "--mode", dest="encrypt_mode",
                            help="Encryption mode (ZIP,LZ4,PCM)", metavar="MODE", choices=["ZIP", "LZ4", "PCM"])

    options = parser.parse_args()

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
    else:
        if options.encrypt_mode is not None:
            encrypt = dalsp_encrypt.DateALive_encryption(options)
            if os.path.isfile(options.input_path):
                encrypt.crypt_single_file()
            else:
                encrypt.crypt_folder()
        else:
            print(
                "Need to use \"-m\" with specified encryption modes: ZIP,LZ4 or PCM. Run \"python main.py -h\" for "
                "more details")
            return


if __name__ == "__main__":
    main()
