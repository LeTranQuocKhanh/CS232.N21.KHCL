from PIL import Image
import struct
import os

def compress_lzw_png(input_path, output_path):
    # Open image and convert to raw pixel data
    with Image.open(input_path) as img:
        raw_data = img.convert("RGB").tobytes()
        original_size = len(raw_data)

    # Initialize dictionary with all possible byte values
    dictionary = {bytes([i]): i for i in range(256)}

    # Compress data using LZW algorithm
    compressed_data = bytearray()
    current_sequence = bytes()
    code = 256
    for byte in raw_data:
        symbol_sequence = current_sequence + bytes([byte])
        if symbol_sequence in dictionary:
            current_sequence = symbol_sequence
        else:
            compressed_data += struct.pack(">Q", dictionary[current_sequence])
            dictionary[symbol_sequence] = code
            code += 1
            current_sequence = bytes([byte])

    # Pack final code and write compressed data to output file
    if current_sequence:
        compressed_data += struct.pack(">Q", dictionary[current_sequence])
    with open(output_path, "wb") as output_file:
        output_file.write(compressed_data)

    # Compute and print compression ratio
    # original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    print('This is compressed_size', compressed_size)
    compression_ratio = original_size / compressed_size
    print("Compression ratio:", compression_ratio)


compress_lzw_png('large.png', 'image.bin')