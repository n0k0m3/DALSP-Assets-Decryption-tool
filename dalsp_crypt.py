import gzip
import io
import lz4.block
import os
import subprocess
from PIL import Image
import struct
import logging
import sys

# logger to debug.log
FORMAT = "%(name)-25s: %(levelname)-8s %(message)s"
logging.basicConfig(filename='debug.log', filemode='w', format=FORMAT)

# logger to stdout
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter(FORMAT)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


class initWithMNGData:
    def __init__(self, dal_dec, buff):
        self.dal_dec = dal_dec
        self.buff = buff
        self.base_ext = os.path.splitext(self.dal_dec.name)[1]
        if self.dal_dec.verbose:
            self.logger = logging.getLogger('initWithMNGData')
            self.logger.setLevel(logging.INFO)
        self.split_PVR()

    def split_PVR(self):
        buff = self.buff[3:]
        image_size = struct.unpack('<I', buff[:4])[0]
        buff = buff[4:]
        image_file = buff[:image_size]
        filepath = os.path.join(self.dal_dec.output_path, self.dal_dec.relpath, self.dal_dec.name)
        try:
            if image_file[:4] == b'RIFF':
                im = Image.open(io.BytesIO(image_file))
                if self.dal_dec.verbose:
                    self.logger.info("Image header format: "+im.format)
                data = io.BytesIO()
                im_format = 'JPEG' if self.base_ext[1:].lower() == 'jpg' else self.base_ext[1:].upper()
                im.save(data, im_format)
                png_file = data.getvalue()
                if self.dal_dec.verbose:
                    self.logger.info("Convert "+im.format+" to "+self.base_ext[1:].upper())
                self.dal_dec.write(filepath, png_file)
            elif image_file[:3] == b'PVR':
                if self.dal_dec.verbose:
                    self.logger.info("Image header format: PVR")
                name = os.path.splitext(self.dal_dec.name)[0] + ".pvr"
                filepath = os.path.join(self.dal_dec.output_path, self.dal_dec.relpath, name)
                self.dal_dec.write(filepath, image_file)
                self.unpack_PVR(filepath)
                filepath = filepath[:-3] + self.base_ext[1:]
            else:
                im = Image.open(io.BytesIO(image_file))
                self.dal_dec.write(filepath, image_file)
                if self.dal_dec.verbose:
                    self.logger.info("Image header format: "+im.format)
                    self.logger.warning(filepath)
                    self.logger.warning("Potentially not supported image format")
        except:
            if self.dal_dec.verbose:
                self.logger.error("An error occured during processing this image file")
                self.logger.error(filepath)
                self.logger.error("Send file to the maintainer for debugging")
            else:
                print("An error occured in file",filepath,". Please enable -v or --verbose to debug")
        buff = buff[image_size:]
        if buff[:4] != b"":
            self.restore_alpha(buff, filepath)

    def restore_alpha(self, buff, filepath):
        alpha_size = struct.unpack('<I', buff[:4])[0]
        buff = buff[4:]
        alpha_file = buff[:alpha_size]
        if alpha_file[:3] == b'PVR':
            name = "alpha_" + os.path.splitext(self.dal_dec.name)[0] + ".pvr"
            filepath_alpha = os.path.join(self.dal_dec.output_path, self.dal_dec.relpath, name)
            self.dal_dec.write(filepath_alpha, alpha_file)
            self.unpack_PVR(filepath_alpha)
            filepath_alpha = filepath_alpha[:-3] + self.base_ext[1:]
        else:
            name = "alpha_" + self.dal_dec.name
            filepath_alpha = os.path.join(self.dal_dec.output_path, self.dal_dec.relpath, name)
            self.dal_dec.write(filepath_alpha, alpha_file)
        try:
            im_rgb = Image.open(filepath).convert("RGB")
            im_a = Image.open(filepath_alpha).convert("L")
            im_rgba = im_rgb.copy()
            im_rgba.putalpha(im_a)
            if self.base_ext[1:].lower() == "jpg":
                im_rgba = im_rgba.convert('RGB')
            im_rgba.save(filepath)
            os.remove(filepath_alpha)
        except:
            if self.dal_dec.verbose:
                self.logger.error("Unknown alpha process scheme in files")
                self.logger.error(filepath)
                self.logger.error(filepath_alpha)
                self.logger.error("Send files to the maintainer for debugging")
            else:
                print("An error occured in file",filepath,". Please enable -v or --verbose to debug")

        buff = buff[alpha_size:]
        if buff != b"":
            if self.dal_dec.verbose:
                self.logger.error("Alpha file size mismatch")
                self.logger.error(filepath)
                self.logger.error("Send files to the maintainer for debugging")
            else:
                print("An error occured in file",filepath,". Please enable -v or --verbose to debug")

    def unpack_PVR(self, filepath):
        if self.dal_dec.unpackPVR and os.path.splitext(filepath)[1] == ".pvr":
            filename = os.path.basename(filepath)
            fileout = os.path.splitext(filepath)[0] + self.base_ext
            plistout = os.path.join(self.dal_dec.output_path, "info.plist")
            with open(os.devnull, 'w') as FNULL:
                if self.dal_dec.verbose:
                    self.logger.info("Unpacking PVR: " + filename)
                command = ["TexturePacker", filepath,
                           "--sheet", fileout, "--data", plistout,
                           "--max-size", "4096"]
                process = subprocess.Popen(
                    command, stdout=FNULL, stderr=subprocess.PIPE)
                _, stderr = process.communicate()
            if self.dal_dec.verbose:
                string = stderr.decode("utf-8")
                if string == "":
                    self.logger.info("Done. No error found.")
                else:
                    self.logger.error("There's an error, maybe need to manually unpack")
                    self.logger.error(filepath)
                    self.logger.error(string)
            if not self.dal_dec.keepPVR:
                os.remove(filepath)


class DateALive_decryption:
    def __init__(self, options):
        self.input_path = options.input_path
        self.keepPVR = options.keepPVR
        self.output_path = options.output_path
        self.overwrite = options.overwrite
        self.unpackPVR = options.unpackPVR
        self.verbose = options.verbose
        if self.verbose:
            self.logger = logging.getLogger('DateALive_decryption')
            self.logger.setLevel(logging.INFO)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def decryptLZ4(data):
        if data[:3] == bytes([0xf8, 0x8b, 0x2b]):
            while data[:3] == bytes([0xf8, 0x8b, 0x2b]):
                data = bytes(data[3:])
                data = lz4.block.decompress(data)
        return data, len(data)

    def decrypt_assets(self):
        data = self.data
        if data[:2] == bytes([0xf8, 0x8b]):
            if data[2] in [0x2d, 0x3d, 0x2b]:
                data, data_size = self.decryptLZ4(data)
                data, retval = self.decryptZIP(data, data_size)
            else:
                retval = -1
        elif data[:3] == bytes([0xFB, 0x1B, 0x9D]):
            data_size = len(data)
            data, retval = self.decryptToPcm(data, data_size)
        else:
            retval = 0
        return data, retval

    @staticmethod
    def write(path, content):
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        open(path, 'wb').write(content)

    def decrypt_file(self):
        file_exist = os.path.join(self.output_path, self.relpath, self.name)
        if not self.overwrite:
            if os.path.isfile(file_exist):
                if self.verbose:
                    print(self.verbose)
                    self.logger.warning(self.name + " already exists at destination, skipping...")
                return
        with open(self.path, "rb") as file:
            self.data = file.read()
            if self.verbose:
                self.logger.info("Reading: " + os.path.join(self.relpath, self.name))
            buff, retval = self.decrypt_assets()
            if self.verbose:
                debug_dict = {
                    -1: "Wrong decryption method, will not write to destination",
                    0: "File is not encrypted, write to destination anyway",
                    1: "Decrypted",
                }
                if retval == 1:
                    self.logger.info(debug_dict[retval])
                else:
                    self.logger.warning(debug_dict[retval])
            if retval != -1:
                if buff[:3] == b"MNG":
                    initWithMNGData(self, buff)
                else:
                    filepath = os.path.join(self.output_path, self.relpath, self.name)
                    self.write(filepath, buff)

    def decrypt_folder(self):
        for root, _, files in os.walk(self.input_path):
            for self.name in files:
                self.relpath = os.path.relpath(root, self.input_path)
                self.path = os.path.join(root, self.name)
                self.decrypt_file()

    def decrypt_single_file(self):
        self.relpath = ""
        self.name = os.path.basename(self.input_path)
        self.path = self.input_path
        self.decrypt_file()


if __name__ == "__main__":
    class options:
        input_path = 'tmp/cap2.mp4'
        output_path = 'tmp_dec/'
        file_mode = True
        verbose = True
        unpackPVR = False
        keepPVR = False
        overwrite = True


    decrypt = DateALive_decryption(options)
    decrypt.decrypt_single_file()
