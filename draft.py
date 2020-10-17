from PIL import Image
import struct
from tex2img import basisu_decompress 

with open("tmp/city_12701.pvr","rb") as f:
    buff = f.read()
    pixel_format = struct.unpack('<I', buff[4*2:4*2+4])[0]
    if pixel_format == 6:
        pixel_format = 0
    elif pixel_format == 2:
        pixel_format = 11
    height = struct.unpack('<I', buff[4*6:4*6+4])[0]
    width = struct.unpack('<I', buff[4*7:4*7+4])[0]
    img=buff[67:]
rgba_data = basisu_decompress(img, width, height, pixel_format)
im = Image.frombytes("RGBA",(width, height),rgba_data)
im.show()