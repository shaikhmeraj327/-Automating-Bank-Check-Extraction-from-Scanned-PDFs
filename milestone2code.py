# milestone 2 codes are as follow.
# milestone 2 codes are as follow.
!pip install pdf2image
!apt-get install poppler-utils

import os
import cv2
from pdf2image import convert_from_path
import matplotlib.pyplot as plt

def pdf_to_images(pdf_path, output_dir):
    """
    Converts a PDF file to a series of images, one for each page.
    """
    pages = convert_from_path(pdf_path)
    page_image_paths = []
    for i, page in enumerate(pages):
        page_filename = os.path.join(output_dir, f"page_{i + 1}.jpg")
        page.save(page_filename, "JPEG")
        page_image_paths.append(page_filename)
        print(f"Saved page {i + 1} as image: {page_filename}")
    return page_image_paths

def display_image(image_path):
    """
    Displays an image using matplotlib.
    """
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 8))
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.show()

def extract_and_save_checks(image_path, output_dir, page_number=1):
    """
    Extracts check regions from an image and saves them as separate images.
    Displays each check's details only once per page.
    """
    print(f"\nProcessing image for page {page_number}: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image {image_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    check_count = 0
    checks = []  # List to hold check regions

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        if 1000 < w * h < 500000 and 2.0 < aspect_ratio < 4.0:  # Check size and aspect ratio
            check = image[y:y+h, x:x+w]
            page_output_dir = os.path.join(output_dir, f"page_{page_number}")
            os.makedirs(page_output_dir, exist_ok=True)
            check_filename = f"check_{check_count + 1}.jpg"
            check_output_path = os.path.join(page_output_dir, check_filename)
            cv2.imwrite(check_output_path, check)
            checks.append({'filename': check_output_path, 'bbox': (x, y, w, h)})
            check_count += 1

    # Only print the total and check information once per page
    print(f"Total checks extracted from page {page_number}: {check_count}")
    if check_count > 0:
        print(f"Extracted checks saved for page {page_number}:")
        for check in checks:
            print(f"  - {check['filename']}")
    else:
        print(f"No checks found on page {page_number}.")


# Main execution
pdf_path = "cheque_1 (1).pdf"  # Updated with the correct path to your PDF file
output_images_dir = "pdf_pages"
output_checks_dir = "extracted_checks"

# Step 1: Convert PDF to images
os.makedirs(output_images_dir, exist_ok=True)
page_image_paths = pdf_to_images(pdf_path, output_images_dir)

# Step 2: Display each PDF page image and then extract checks
for i, image_path in enumerate(page_image_paths):
    print(f"\nDisplaying page {i + 1}:")
    display_image(image_path)  # Display the image of the PDF page
    extract_and_save_checks(image_path, output_checks_dir, page_number=i + 1)
