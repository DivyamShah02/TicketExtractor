from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException
from library.GetLogger import apply_logs_to_all_methods, log
import time
import os

@apply_logs_to_all_methods(log)
class ChromeHandler:
    def __init__(self, logger, config) -> None:
        self.logger = logger
        self.config = config
        self.driver = None
        # self.kill_all_chrome()

    def kill_all_chrome(self) -> None:
        """Terminate all Chrome processes."""
        try:
            self.logger.info("Terminating all Chrome processes.")
            # os.system("taskkill /F /IM chrome.exe")
            self.logger.info("All Chrome processes terminated.")
        except Exception as e:
            self.logger.error("Failed to terminate Chrome processes.", exc_info=True)

    def start_chrome(self) -> bool:
        """Start Chrome browser using Selenium."""
        try:
            self.logger.info("Starting Chrome with Selenium WebDriver.")
            chrome_options = Options()
            prefs = {
                "download.default_directory": self.config.paths.download_path,  # Set custom download directory
                "download.prompt_for_download": False,  # Disable download prompt
                "profile.default_content_settings.popups": 0,  # Disable pop-ups
                "directory_upgrade": True  # Ensure that the directory exists and upgrade it if necessary
            }
            chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            self.logger.info("Chrome started successfully.")
            return True
        except WebDriverException as e:
            self.logger.error("Error while starting Chrome with Selenium.", exc_info=True)
            return False

    def maximise_chrome(self) -> bool:
        """Maximize Chrome window."""
        try:
            self.logger.info("Maximizing Chrome window.")
            self.driver.maximize_window()
            self.logger.info("Chrome window maximized successfully.")
            return True
        except WebDriverException as e:
            self.logger.error("Error while maximizing Chrome window.", exc_info=True)
            return False

    def load_url(self, url: str) -> bool:
        """Load a specific URL in Chrome."""
        try:
            self.logger.info(f"Loading URL: {url}")
            self.driver.get(url)
            self.logger.info(f"URL {url} loaded successfully.")
            return True
        except WebDriverException as e:
            self.logger.error(f"Error while loading URL: {url}", exc_info=True)
            return False

    def scroll_to_end_of_page(self) -> None:
        """Scroll to the end of the web page."""
        try:
            self.logger.info("Scrolling to the end of the page.")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.logger.info("Successfully scrolled to the end of the page.")
            return True
        except Exception as e:
            self.logger.error("Error occurred while scrolling to the end of the page.", exc_info=True)
            return False

    def click_button_by_xpath(self, xpath: str) -> bool:
        """Dynamically click on a button using the provided XPath."""
        try:
            self.driver.implicitly_wait(10)  # Optional: Implicit wait for the element to be present
            self.logger.info(f"Attempting to click button with XPath: {xpath}")
            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
            self.logger.info(f"Successfully clicked the button with XPath: {xpath}")
            return True
        except NoSuchElementException:
            self.logger.error(f"Element not found with XPath: {xpath}", exc_info=True)
            return False
        except ElementClickInterceptedException:
            self.logger.error(f"Element with XPath: {xpath} could not be clicked.", exc_info=True)
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while clicking the button with XPath: {xpath}", exc_info=True)
            return False

    def template_fun(self) -> bool:
        """Placeholder function for custom logic."""
        try:
            self.logger.info("Executing template function.")
            # Custom logic using Selenium goes here
            self.logger.info("Template function executed successfully.")
            return True
        except Exception as e:
            self.logger.error("Error while executing template function.", exc_info=True)
            return False

    def quit_chrome(self) -> None:
        """Quit Chrome browser."""
        try:
            self.logger.info("Quitting Chrome.")
            if self.driver:
                self.driver.quit()
            self.logger.info("Chrome quit successfully.")
        except WebDriverException as e:
            self.logger.error("Error while quitting Chrome.", exc_info=True)
