import io
import logging
import os
import struct
import sys
import zlib

import lz4.block
import numpy as np
from PIL import Image
from tex2img import basisu_decompress


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
        filepath = os.path.join(self.dal_dec.output_path,
                                self.dal_dec.relpath, self.dal_dec.name)
        buff = self.buff[3:]
        image_size = struct.unpack('<I', buff[:4])[0]
        buff = buff[4:]
        image_file = self.unpack_PVR(buff[:image_size], "")
        buff = buff[image_size:]
        if buff[:4] != b"":  # Restoring Alpha Channel
            alpha_size = struct.unpack('<I', buff[:4])[0]
            buff = buff[4:]
            alpha_file = self.unpack_PVR(buff[:alpha_size], "alpha_")
            try:
                im_rgb = Image.open(io.BytesIO(image_file)).convert("RGB")
                im_a = Image.open(io.BytesIO(alpha_file)).convert("L")
                im_rgba = im_rgb.copy()
                im_rgba.putalpha(im_a)
                with io.BytesIO() as output:
                    im_rgba = im_rgba.convert(
                        'RGB') if self.base_ext[1:].lower() == 'jpg' else im_rgba
                    im_format = 'JPEG' if self.base_ext[1:].lower(
                    ) == 'jpg' else self.base_ext[1:].upper()
                    im_rgba.save(output, format=im_format)
                    self.dal_dec.write(filepath, output.getvalue())
            except:
                if self.dal_dec.verbose:
                    self.logger.error("Unknown alpha process scheme in files")
                    self.logger.error(filepath)
                    self.logger.error(
                        "Send files to the maintainer for debugging")
                else:
                    print("An error occured in file", filepath,
                          ". Please enable -v or --verbose to debug")
            buff = buff[alpha_size:]
            if buff != b"":
                if self.dal_dec.verbose:
                    self.logger.error("Alpha file size mismatch")
                    self.logger.error(filepath)
                    self.logger.error(
                        "Send files to the maintainer for debugging")
                else:
                    print("An error occured in file", filepath,
                          ". Please enable -v or --verbose to debug")
        else:
            self.save_image(image_file, filepath)

    def save_image(self, image_file, filepath):
        try:
            if image_file[:4] == b'RIFF':
                im = Image.open(io.BytesIO(image_file))
                if self.dal_dec.verbose:
                    self.logger.info("Image header format: " + im.format)
                old_format = im.format
                data = io.BytesIO()
                im = im.convert(
                    'RGB') if self.base_ext[1:].lower() == 'jpg' else im
                im_format = 'JPEG' if self.base_ext[1:].lower(
                ) == 'jpg' else self.base_ext[1:].upper()
                im.save(data, im_format)
                png_file = data.getvalue()
                if self.dal_dec.verbose:
                    self.logger.info("Convert " + old_format +
                                     " to " + self.base_ext[1:].upper())
                self.dal_dec.write(filepath, png_file)
            else:
                im = Image.open(io.BytesIO(image_file))
                self.dal_dec.write(filepath, image_file)
                if self.dal_dec.verbose:
                    self.logger.info("Image header format: " + im.format)
                    if im.format not in ["JPEG"]:
                        self.logger.warning(filepath)
                        self.logger.warning(
                            "Potentially not supported image format")
        except:
            if self.dal_dec.verbose:
                self.logger.error(
                    "An error occured during processing this image file")
                self.logger.error(filepath)
                self.logger.error("Send file to the maintainer for debugging")
            else:
                print("An error occured in file", filepath,
                      ". Please enable -v or --verbose to debug")

    def unpack_PVR(self, buff, name):
        if buff[:3] != b"PVR":
            return buff
        if self.dal_dec.keepPVR:
            base_name = os.path.splitext(self.dal_dec.name)[0]
            filepath = os.path.join(self.dal_dec.output_path,
                                    self.dal_dec.relpath, name + base_name + ".pvr")
            self.dal_dec.write(filepath, buff)
        pixel_format = struct.unpack('<I', buff[4 * 2:4 * 2 + 4])[0]
        if pixel_format == 6:
            mode = 0
        elif pixel_format == 2:
            mode = 11
        height = struct.unpack('<I', buff[4 * 6:4 * 6 + 4])[0]
        width = struct.unpack('<I', buff[4 * 7:4 * 7 + 4])[0]
        img = buff[67:]
        rgba_data = basisu_decompress(img, width, height, mode)
        im = Image.frombytes("RGBA", (width, height), rgba_data)
        with io.BytesIO() as result:
            im = im.convert(
                'RGB') if self.base_ext[1:].lower() == 'jpg' else im
            im_format = 'JPEG' if self.base_ext[1:].lower(
            ) == 'jpg' else self.base_ext[1:].upper()
            im.save(result, format=im_format)
            result = result.getvalue()
        return result


class DateALive_decryption:
    def __init__(self, options):
        self.input_path = options.input_path
        self.keepPVR = options.keepPVR
        self.output_path = options.output_path
        self.overwrite = options.overwrite
        self.verbose = options.verbose
        if self.verbose:
            # logger to debug.log
            FORMAT = "%(name)-25s: %(levelname)-8s %(message)s"
            logging.basicConfig(filename='../debug.log',
                                filemode='w', format=FORMAT)

            # logger to stdout
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            formatter = logging.Formatter(FORMAT)
            console.setFormatter(formatter)
            logging.getLogger().addHandler(console)
            output_file_handler = logging.FileHandler("debug.log")
            output_file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(FORMAT)
            output_file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(output_file_handler)
            self.logger = logging.getLogger('DateALive_decryption')
            self.logger.setLevel(logging.INFO)

    @staticmethod
    def decryptZIP(data:bytes, data_size:int)->bytes:
        if data[:2] == bytes([0xf8, 0x8b]) and data[2] in [0x2d, 0x3d]:

            # From bytearray to np array
            data = np.array(np.frombuffer(data, np.uint8))

            # Reform DEFLATE header
            data[1] = 0x1f
            data[2] = 0x8b

            # decryptZIP
            var_1 = 0x14

            if (data_size - 3) < 0x15:
                var_1 = data_size - 3
            if 0 < var_1:
                i = 2
                n = var_1 + 2

            data = data[1:]

            var_1_array = data[i:n-1]
            var_1_array = (np.cumsum(var_1_array)+0x14) % 0x2d
            var_1_array = np.append([var_1], var_1_array).astype(int)

            data[i:n] = data[i:n] ^ var_1_array
            data = data.tobytes()

            # Decompress zlib
            data = zlib.decompress(data, zlib.MAX_WBITS | 32)

        return data, 1

    @staticmethod
    def decryptToPcm(data:bytes, data_size:int)->bytes:
        data = bytearray(data)
        while data[:3] == bytes([0xFB, 0x1B, 0x9D]):
            xor_var = data[3]
            # n = data_size - 4
            buff = data[4:]
            if 4 < data_size:
                buff = np.array(buff)
                buff = buff ^ xor_var
                buff = bytearray(buff.tobytes())
            data = buff
            data_size = len(data)
        return bytes(data), 1

    @staticmethod
    def decryptLZ4(data:bytes)->bytes:
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

    def crypt_file(self):
        file_exist = os.path.join(self.output_path, self.relpath, self.name)
        if not self.overwrite:
            if os.path.isfile(file_exist):
                if self.verbose:
                    self.logger.warning(
                        self.name + " already exists at destination, skipping...")
                return
        with open(self.path, "rb") as file:
            self.data = file.read()
            if self.verbose:
                self.logger.info(
                    "Reading: " + os.path.join(self.relpath, self.name))
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
                    filepath = os.path.join(
                        self.output_path, self.relpath, self.name)
                    self.write(filepath, buff)

    def crypt_folder(self):
        for root, _, files in os.walk(self.input_path):
            for self.name in files:
                self.relpath = os.path.relpath(root, self.input_path)
                self.path = os.path.join(root, self.name)
                self.crypt_file()

    def crypt_single_file(self):
        self.relpath = ""
        self.name = os.path.basename(self.input_path)
        self.path = self.input_path
        self.crypt_file()


if __name__ == "__main__":
    class options:
        input_path = 'tmp/cap2.mp4'
        output_path = '../tmp_dec/'
        file_mode = True
        verbose = True
        keepPVR = False
        overwrite = True

    decrypt = DateALive_decryption(options)
    decrypt.crypt_single_file()
