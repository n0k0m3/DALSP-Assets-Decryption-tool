import dalsp_crypt
from optparse import OptionParser


def main():
    print("Date A Live: Spirit Pledge Assets Decryption tool\n")
    print("Decrypt all assets in source directory and save in destination directory\n")
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_path",
                      help="Encrypted Data Source (folder/file; if file, use -f)", metavar="\"INPUT\"")
    parser.add_option("-o", "--output", dest="output_path",
                      help="Decrypted Data Destination (MUST BE A FOLDER)", metavar="\"OUTPUT\"")
    parser.add_option("-f", "--file", dest="file_mode",
                      action="store_true", default=False,
                      help="Single file decryption mode")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print status messages to stdout")

    (options, args) = parser.parse_args()

    if options.input_path == None or options.output_path == None:
        print()
        print("No input or output path specified. Run \"python main.py -h\" for more details")
        print()
        return
    if not options.file_mode:
        dalsp_crypt.decrypt_folder(options)
    else:
        dalsp_crypt.decrypt_single_file(options)


if __name__ == "__main__":
    main()
