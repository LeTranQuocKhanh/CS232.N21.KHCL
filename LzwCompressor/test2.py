import struct
from PIL import Image

def decompress_lzw_png(compressed_path):
    # Read the compressed data from the file
    with open(compressed_path, "rb") as f:
        compressed_data = f.read()

    # Decompress the data using LZW
    table = {i: bytes([i]) for i in range(256)}
    next_code = 256
    string = b""
    output_data = b""
    for i in range(0, len(compressed_data), 2):
        code = struct.unpack(">H", compressed_data[i:i+2])[0]
        if code not in table:
            new_string = string + bytes([string[0]])
        else:
            new_string = table[code]
        output_data += new_string
        if string:
            table[next_code] = string + bytes([new_string[0]])
            next_code += 1
        string = new_string

    # Convert the raw image data to a PNG image and save it
    return output_data

print(decompress_lzw_png('image.bin'))