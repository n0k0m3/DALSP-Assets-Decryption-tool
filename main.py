import dalsp_crypt
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_path",
                      help="Encrypted Data Directory", metavar="\"DIR_IN\"")
    parser.add_option("-o", "--output", dest="output_path",
                      help="Decrypted Data Directory", metavar="\"DIR_OUT\"")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print status messages to stdout")

    (options, args) = parser.parse_args()

    if options.input_path == None or options.output_path == None:
        print()
        print("No input or output path specified. Run \"python main.py -h\" for more details")
        print()
        return
    dalsp_crypt.decrypt_folder(options)

if __name__ == "__main__":
    main()
