from pdf2image import convert_from_path

# this is to check if the pdf to image conversion is working fine because I installed poppler and set the path, this is required for it to work

pdf_path = r"C:\Users\HP\Downloads\EXAMPLE_IMAGE_1.pdf"
poppler_path = r"C:\poppler\poppler-24.08.0\Library\bin"

pages = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)
print("Pages converted:", len(pages))
pages[0].save("test_output.jpg", "JPEG")
print("Image saved as test_output.jpg")
