import fitz  # PyMuPDF

def crop_pdf_from_bottom(input_pdf, output_pdf, crop_height):
    # Open the PDF file
    doc = fitz.open(input_pdf)
    
    # Iterate over all the pages
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Get the original page dimensions
        original_rect = page.rect
        # Define the new rectangle (crop from the bottom)
        new_rect = fitz.Rect(original_rect.x0, original_rect.y0, original_rect.x1, original_rect.y1 - crop_height)
        # Set the new crop box
        page.set_cropbox(new_rect)
    
    # Save the cropped PDF to a new file
    doc.save(output_pdf)
    doc.close()

def cover_area_in_scanned_pdf(input_pdf, output_pdf, x0, y0, x1, y1):
    # Open the PDF file
    doc = fitz.open(input_pdf)
    
    # Iterate over all the pages (or specify a specific page if needed)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Define the rectangle coordinates (x0, y0, x1, y1)
        rect = fitz.Rect(x0, y0, x1, y1)
        
        # Draw a white rectangle over the specified area
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))  # Draw white rectangle
    
    # Save the modified PDF to a new file
    doc.save(output_pdf)
    doc.close()

# Example usage
input_pdf = r"C:\Users\LENOVO\Desktop\Dynamic Labz\Ticket_Downloader\Downloaded_Files\FFGZAQ.pdf"
output_pdf = r"C:\Users\LENOVO\Desktop\Dynamic Labz\Ticket_Downloader\Downloaded_Files\output.pdf"
crop_height = 160  # Amount to crop from the bottom in points (1 point = 1/72 inches)

x0, y0, x1, y1 = 50, 820, 550, 850  # Coordinates to just remove the price
x0, y0, x1, y1 = 50, 800, 550, 850  # Coordinates to remove total price text

cover_area_in_scanned_pdf(input_pdf, output_pdf, x0, y0, x1, y1)

# crop_pdf_from_bottom(input_pdf, output_pdf, crop_height)
