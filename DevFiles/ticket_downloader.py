import fitz
import os
import sys
import pdb
import time
import shutil
import pandas as pd
import pyautogui as pg
import pyperclip as pyc
from library.Config import Config
from library.GetLogger import GetLogger
from library.ChromeHandler import ChromeHandler

def main():
    """Main function to automate Chrome tasks."""
    try:
        start_time = time.time()
        cwd_path = os.getcwd()
        config_path = cwd_path.replace('DevFiles', 'BotConfig\\config.ini')
        config = Config(filename=config_path)

        logs_dir = config.paths.logs_path
        logger = GetLogger(log_file_dir=logs_dir, log_file_name="chrome_automater.log", file_handler=True).logger

        chrome_handler = ChromeHandler(logger=logger, config=config)

        if not chrome_handler.start_chrome():
            logger.error("Failed to start Chrome.")
            sys.exit(1)

        if not chrome_handler.maximise_chrome():
            logger.error("Failed to maximize Chrome.")
            chrome_handler.kill_all_chrome()
            sys.exit(1)

        excel_files = [file for file in os.listdir(config.paths.unprocessed_path) if file.lower().endswith('.xlsx')]

        for excel in excel_files:
            process_excel_file(excel, config, chrome_handler, logger)
            process_pdfs(config, logger)
            gen_processed_fol(excel, config, logger)
            archive_file(excel, config)


        chrome_handler.kill_all_chrome()
        logger.info("Chrome automation completed successfully.")
        end_time = time.time()

        logger.info(f'# Total time taken in execution : {end_time - start_time}')

    except Exception as e:
        logger.error("An unexpected error occurred.", exc_info=True)
        sys.exit(1)

def write_in_url_bar(value):
    try:
        pg.hotkey('ctrl', 'l')
        pg.hotkey('ctrl', 'a')
        pg.press('backspace')
        pg.write(value)
        time.sleep(0.2)
    
    except Exception as e:
        pass

def process_excel_file(excel, config, chrome_handler, logger):
    """Process each Excel file for data extraction."""
    try:
        df = pd.read_excel(os.path.join(config.paths.unprocessed_path, excel))
        number_lst = []
        error_lst = []

        for ind, row in df.iterrows():
            if not chrome_handler.load_url(url=row['Ticket Link']):
                logger.error("Failed to load URL for row %d.", ind)
                error_lst.append(row)
                continue

            if not chrome_handler.scroll_to_end_of_page():
                logger.error("Failed to scroll to end for row %d.", ind)
                error_lst.append(row)
                continue
            
            if not chrome_handler.click_button_by_xpath(xpath=str(config.Selenium_Details.download_btn_xpath).replace("'", "")):
                logger.error("Failed to click on download button for row %d.", ind)
                error_lst.append(row)
                continue
            time.sleep(1)
        # save_results(number_lst, error_lst, excel, config)

    except Exception as e:
        logger.error("Error processing file %s: %s", excel, e, exc_info=True)
        raise

def save_results(number_lst, error_lst, excel, config):
    """Save results to Excel files and handle naming conflicts."""
    try:
        if number_lst:
            number_df = pd.DataFrame(number_lst)
            processed_file_name = generate_file_name(folder=config.paths.processed_path, file_name=excel)
            number_df.to_excel(processed_file_name, index=False)

        if error_lst:
            error_df = pd.DataFrame(error_lst)
            error_file_name = generate_file_name(folder=config.paths.error_path, file_name=excel)
            error_df.to_excel(error_file_name, index=False)
    except Exception as e:
        raise RuntimeError(f"Error saving results: {e}")

def archive_file(excel, config):
    """Move processed file to archive."""
    try:
        archive_file_name = generate_file_name(folder=config.paths.archive_path, file_name=excel)
        shutil.move(os.path.join(config.paths.unprocessed_path, excel), archive_file_name)
    except Exception as e:
        raise RuntimeError(f"Error archiving file {excel}: {e}")

def generate_file_name(folder, file_name):
    """Generate unique file name to avoid conflicts."""
    process_file_path = os.path.join(folder, file_name)
    counter = 1
    while os.path.exists(process_file_path):
        base_name, ext = os.path.splitext(file_name)
        base_name = str(base_name).replace(f'_{counter-1}','')
        process_file_path = os.path.join(folder, f"{base_name}_{counter}{ext}")
        counter += 1
    return process_file_path

def process_pdfs(config, logger):
    try:
        all_pdfs = [file for file in os.listdir(config.paths.download_path) if file.lower().endswith('.pdf')]
        for pdf in all_pdfs:
            try:
                logger.info(f'Processing {pdf}')
                input_pdf = os.path.join(config.paths.download_path, pdf)
                output_pdf = os.path.join(config.paths.edited_path, pdf)
                x0, y0, x1, y1 = 50, 820, 550, 850  # Coordinates to just remove the price
                x0, y0, x1, y1 = 50, 800, 550, 850  # Coordinates to remove total price text
                cover_area_in_scanned_pdf(input_pdf, output_pdf, x0, y0, x1, y1)
                try:
                    # shutil.move(input_pdf, os.path.join(config.paths.archive_path, pdf))
                    os.remove(input_pdf)
                except:
                    pass
                logger.info(f'Processed {pdf}')

            except Exception as e:
                logger.error(f"Error while processing {pdf} - {e}", exc_info=True)

        return True

    except Exception as e:
        logger.error(f"Error while processing pdfs {e}", exc_info=True)
        return False

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

def gen_processed_fol(excel, config, logger):
    try:
        excel_name = excel.replace('.xlsx', '')
        folder_name = generate_file_name(folder=config.paths.processed_path, file_name=excel_name)
        os.mkdir(folder_name)
        df = pd.read_excel(os.path.join(config.paths.unprocessed_path, excel))
        for ind,row in df.iterrows():
            try:
                code = str(row['Shortcode'])
                downloaded_path = os.path.join(config.paths.edited_path, f'{code}.pdf')
                if os.path.exists(downloaded_path):
                    shutil.move(downloaded_path, os.path.join(folder_name, f'{code}.pdf'))
            except Exception as ex:
                logger.error(f'Error occured in {excel} at{ind}')
    except Exception as e:
        logger.error(e, exc_info=True)

if __name__ == "__main__":
    main()
