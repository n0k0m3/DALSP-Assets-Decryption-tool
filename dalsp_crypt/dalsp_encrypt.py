import logging
import os
import zlib
from random import randint

import lz4.block

from dalsp_crypt.dalsp_decrypt import DateALive_decryption


class DateALive_encryption(DateALive_decryption):
    def __init__(self, options):
        super().__init__(options)
        if self.verbose:
            self.logger = logging.getLogger('DateALive_encryption')
            self.logger.setLevel(logging.INFO)
        self.encrypt_mode = options.encrypt_mode.lower()

    def crypt_file(self):
        with open(self.path, "rb") as file:
            self.data = file.read()
        if self.verbose:
            self.logger.info(
                "Reading: " + os.path.join(self.relpath, self.name))
        try:
            decrypt_method = getattr(
                self, "encrypt" + str(self.encrypt_mode.split(",")[0]).upper())
            buff, retval = decrypt_method(self.data)
            if self.verbose:
                self.logger.info("Encrypted")
        except AttributeError:
            if self.verbose:
                self.logger.error("Encryption mode doesn't exist")
            return
        if retval != -1:
            filepath = os.path.join(self.output_path, self.relpath, self.name)
            self.write(filepath, buff)

    @staticmethod
    def encryptZIP(data):
        gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
        data = gzip_compress.compress(data) + gzip_compress.flush()
        data = bytearray([0xf8]) + data
        data[10] = 0x03  # Force OS = Unix
        data_size = len(data)
        var_1 = 0x14
        if (data_size - 3) < int(str(0x15)):
            var_1 = data_size - 3
        if 0 < var_1:
            i = 2
            n = var_1 + 2
        while True:
            var_2 = var_1 % 0x2d
            data[i + 1] = var_2 ^ data[i + 1]
            var_1 = data[i + 1] + var_2
            i = i + 1
            if not (i < n):
                break
        data[1] = 0x8b
        data[2] = 0x2d
        return data, 1

    @staticmethod
    def encryptLZ4(data):
        data = bytearray(lz4.block.decompress(data))
        return bytearray([0xf8, 0x8b, 0x2b]) + data, 1

    def encryptPCM(self, data):
        data = bytearray(data)
        data_size = len(data)
        n = data_size
        if len(self.encrypt_mode.split(",")) > 1:
            xor_var = int("0x" + self.encrypt_mode.split(",")[1], 16)
        else:
            xor_var = randint(0, 0xFF)
        if 4 < data_size:
            i = 0
            while True:
                n = n - 1
                data[i] = data[i] ^ xor_var
                i = i + 1
                if not (n != 0):
                    break
        return bytearray([0xFB, 0x1B, 0x9D, xor_var]) + data, 1


if __name__ == "__main__":
    pass
