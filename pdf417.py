from PIL import Image as PIL
from pdf417decoder import PDF417Decoder

# Open the image containing the PDF417 barcode
image = PIL.open("barcode.png")

# Create a PDF417Decoder object
decoder = PDF417Decoder(image)

# Attempt to decode the barcode
if (decoder.decode() > 0):
    # Retrieve the decoded data from the first barcode
    decoded_data = decoder.barcode_data_index_to_string(0)
    print(f"{decoded_data}")
else:
    print("No PDF417 barcode found in the image.")