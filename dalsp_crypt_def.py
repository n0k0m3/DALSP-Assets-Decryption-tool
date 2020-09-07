import gzip
import io
import lz4.block
import os
import subprocess
from PIL import Image
import struct


def decryptZIP(data, data_size):
    data = bytearray(data)
    if data[:2] == bytes([0xf8, 0x8b]) and data[2] in [0x2d, 0x3d]:
        data[1] = 0x1f
        data[2] = 0x8b
        var_1 = 0x14
        if (data_size - 3) < int(str(0x15)):
            var_1 = data_size - 3
        if 0 < var_1:
            i = 2
            n = var_1 + 2
        while True:
            var_2 = var_1 % 0x2d
            var_1 = data[i + 1] + var_2
            data[i + 1] = var_2 ^ data[i + 1]
            i = i + 1
            if not (i < n):
                break
        data = gzip.decompress(data[1:])
    return data, 1


def decryptToPcm(data, data_size):
    data = bytearray(data)
    while data[:3] == bytes([0xFB, 0x1B, 0x9D]):
        xor_var = data[3]
        n = data_size - 4
        buff = data[4:]
        if 4 < data_size:
            i = 0
            while True:
                n = n - 1
                buff[i] = buff[i] ^ xor_var
                i = i + 1
                if not (n != 0):
                    break
        data = buff
        data_size = len(data)
    return bytes(data), 1


def decryptLZ4(data):
    if data[:3] == bytes([0xf8, 0x8b, 0x2b]):
        while data[:3] == bytes([0xf8, 0x8b, 0x2b]):
            data = bytes(data[3:])
            data = lz4.block.decompress(data)
        # while data[:3] == b"MNG":
        #     data_size = struct.unpack('<I', data[3:7])[0]
        #     if data[data_size+7:] != b'':
        #         print("Exist alpha data")
        #     else:
        #         print("Data is completed")
        #     data = data[7:]
        # im = Image.open(io.BytesIO(data))
        # data = io.BytesIO()
        # im.save(data, "png")
        # data = data.getvalue()
    return data, len(data)


def decrypt_assets(data):
    if data[:2] == bytes([0xf8, 0x8b]):
        if data[2] in [0x2d, 0x3d, 0x2b]:
            data, data_size = decryptLZ4(data)
            data, retval = decryptZIP(data, data_size)
        else:
            retval = -1
    elif data[:3] == bytes([0xFB, 0x1B, 0x9D]):
        data_size = len(data)
        data, retval = decryptToPcm(data, data_size)
    else:
        retval = 0
    return data, retval


def write(path, content):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    open(path, 'wb').write(content)


def unpack_PVR(filepath, options, base_ext):
    if options.unpackPVR and os.path.splitext(filepath)[1] == ".pvr":
        filename = os.path.basename(filepath)
        fileout = os.path.splitext(filepath)[0] + base_ext
        plistout = os.path.join(options.output_path, "info.plist")
        with open(os.devnull, 'w') as FNULL:
            if options.verbose:
                print("Unpacking PVR: ", filename)
            command = ["TexturePacker", filepath,
                       "--sheet", fileout, "--data", plistout,
                       "--max-size", "4096"]
            process = subprocess.Popen(
                command, stdout=FNULL, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
        if options.verbose:
            string = stderr.decode("utf-8")
            if string == "":
                print("Done. No error found.")
                if not options.keepPVR:
                    os.remove(filepath)
            else:
                print("There's an error, need to manually unpack")
                print(string)
            print()


def decrypt_file(path, relpath, name, output_path, options):
    base_ext = os.path.splitext(name)[1]
    fileexist = os.path.join(output_path, relpath, name)
    if not options.overwrite:
        if os.path.isfile(fileexist):
            if options.verbose:
                print(name, "already exists at destination, skipping...")
            return
    with open(path, "rb") as file:
        data = file.read()
        if options.verbose:
            print("Reading:", os.path.join(relpath, name))
        buff, retval = decrypt_assets(data)
        # while buff[:3] == b"MNG":
        #     lead = struct.unpack('<I', buff[3:7])[0]+7
        #     alphabuf = buff[7+lead:]
        #     alphalead = struct.unpack('<I', alphabuf[:4])[0]
        #     buff = buff[7:]
        # if buff[:3] == b"PVR":
        #     name = os.path.splitext(name)[0] + ".pvr"
        if options.verbose:
            debug_dict = {
                -1: "Wrong decryption method, will not write to destination",
                0: "File is not encrypted, write to destination anyway",
                1: "Decrypted",
            }
            print(debug_dict[retval])
            print()
        if retval != -1:
            filepath = os.path.join(output_path, relpath, name)
            write(filepath, buff)
            #unpack_PVR(filepath, options, base_ext)


def decrypt_folder(options):
    input_path = options.input_path
    output_path = options.output_path
    for root, dirs, files in os.walk(input_path):
        for name in files:
            relpath = os.path.relpath(root, input_path)
            path = os.path.join(root, name)
            decrypt_file(path, relpath, name, output_path, options)


def decrypt_single_file(options):
    input_path = options.input_path
    output_path = options.output_path
    relpath = ""
    name = os.path.basename(input_path)
    decrypt_file(input_path, relpath, name, output_path, options)


if __name__ == "__main__":
    class options:
        input_path = 'tmp/cap2.mp4'
        output_path = 'tmp_dec/'
        file_mode = False
        verbose = True


    decrypt_single_file(options)
