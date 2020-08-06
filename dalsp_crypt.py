import gzip
import os
import sys
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
        print("No input or output path specified. Run \"python dalsp_crypt.py -h\" for more details")
        print()
        return

    def decrypt_assets(data):
        param_1 = list(data)
        param_2 = len(param_1)
        if param_1[0] == 0xf8 and param_1[1] == 0x8b:
            if param_1[2] == 0x2d or param_1[2] == 0x3d:
                param_1[1] = 0x1f
                param_1[2] = 0x8b
                uVar3 = 0x14
                if (param_2 - 3) < int(str(0x15)):
                    uVar3 = param_2 - 3
                if 0 < uVar3:
                    iVar4 = 2
                    iVar1 = uVar3 + 2
                while True:
                    uVar2 = uVar3 % 0x2d
                    uVar3 = param_1[iVar4 + 1] + uVar2
                    param_1[iVar4 + 1] = uVar2 ^ param_1[iVar4 + 1]
                    iVar4 = iVar4 + 1
                    if not (iVar4 < iVar1):
                        break
                data = gzip.decompress(bytes(param_1[1:]))
                retval = 1
            else:
                retval = -1
        else:
            retval = 0
        return data, retval

    def write(path, content):
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        open(path, 'wb').write(content)

    def decrypt_folder(input, output):
        for root, dirs, files in os.walk(input):
            for name in files:
                relpath = os.path.relpath(root, input)
                path = os.path.join(root, name)
                with open(path, "rb") as file:
                    data = file.read()
                    if options.verbose:
                        print("Reading:", os.path.join(relpath, name))
                    buff, retval = decrypt_assets(data)
                    if options.verbose:
                        debug_dict = {
                            -1 : "Wrong decryption method, write to destination anyway",
                            0 : "File is not encrypted, write to destination anyway",
                            1 : "Decrypted",
                        }
                        print(debug_dict[retval])
                    write(os.path.join(output, relpath, name), buff)

    decrypt_folder(options.input_path, options.output_path)


if __name__ == "__main__":
    main()
