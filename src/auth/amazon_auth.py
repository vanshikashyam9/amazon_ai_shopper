from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
from dotenv import load_dotenv

class AmazonAuthenticator:
    def __init__(self):
        load_dotenv('config/config.env')
        self.email = os.getenv('AMAZON_EMAIL')
        self.password = os.getenv('AMAZON_PASSWORD')
        self.driver = None

    def initialize_driver(self):
        """Initialize the Chrome WebDriver with appropriate options"""
        options = webdriver.ChromeOptions()
        
        # Add options to make detection harder
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add a user agent to appear more like a regular browser
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Create the driver
        self.driver = webdriver.Chrome(options=options)
        
        # Execute CDP commands to prevent detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def login(self):
        """Handle Amazon login process"""
        try:
            print("Attempting to log in to Amazon...")
            
            # First try to use cookies if available
            cookies_file = 'amazon_cookies.json'
            if os.path.exists(cookies_file):
                print("Found cookies file, attempting to use saved session...")
                self._load_cookies(cookies_file)
                
                # Go to Amazon homepage to check if cookies worked
                self.driver.get('https://www.amazon.com')
                time.sleep(3)
                
                # Check if we're logged in
                try:
                    account_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, "nav-link-accountList"))
                    )
                    print("Login from cookies successful!")
                    return True
                except:
                    print("Cookies expired or invalid, will try manual login...")
            
            # Regular login process as before
            # First visit Amazon homepage to get cookies
            self.driver.get('https://www.amazon.com')
            time.sleep(random.uniform(2, 4))  # Random delay to appear more human-like
            
            # Now go to the signin page
            self.driver.get('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')
            time.sleep(random.uniform(2, 4))
            
            # Wait for email field and enter email with human-like typing
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            self._human_like_typing(email_field, self.email)
            
            # Click continue with a slight delay
            time.sleep(random.uniform(0.5, 1.5))
            continue_button = self.driver.find_element(By.ID, "continue")
            continue_button.click()
            
            # Wait for password field and enter password with human-like typing
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            self._human_like_typing(password_field, self.password)
            
            # Click sign-in with a slight delay
            time.sleep(random.uniform(0.5, 1.5))
            self.driver.find_element(By.ID, "signInSubmit").click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if we're successfully logged in
            try:
                # Look for elements only present when logged in
                account_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "nav-link-accountList"))
                )
                print("Login successful!")
                return True
            except:
                print("Login verification failed - Amazon might be requiring additional verification")
                return False
            
            # After successful login, save cookies for next time
            self._save_cookies(cookies_file)
            
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            # Allow manual login intervention
            print("\n=== MANUAL LOGIN REQUIRED ===")
            print("1. Complete the login process manually in the browser window")
            print("2. Solve any CAPTCHA or verification that appears")
            print("3. Once you're logged in, press Enter to continue...")
            input()
            
            # Save cookies after manual login
            cookies_file = 'amazon_cookies.json'
            self._save_cookies(cookies_file)
            
            # Verify login was successful
            try:
                account_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "nav-link-accountList"))
                )
                print("Manual login successful!")
                return True
            except:
                print("Could not verify login even after manual intervention")
                return False

    def _human_like_typing(self, element, text):
        """Type text in a human-like manner with random delays between keystrokes"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))  # Random delay between keystrokes

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

    def _save_cookies(self, file_path):
        """Save browser cookies to file"""
        import json
        try:
            cookies = self.driver.get_cookies()
            with open(file_path, 'w') as f:
                json.dump(cookies, f)
            print(f"Cookies saved to {file_path}")
        except Exception as e:
            print(f"Error saving cookies: {str(e)}")

    def _load_cookies(self, file_path):
        """Load cookies from file into browser"""
        import json
        try:
            self.driver.get('https://www.amazon.com')  # Need to be on amazon domain to add cookies
            with open(file_path, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    # Some cookies can't be loaded directly, so handle exceptions
                    try:
                        self.driver.add_cookie(cookie)
                    except:
                        pass
            print(f"Cookies loaded from {file_path}")
        except Exception as e:
            print(f"Error loading cookies: {str(e)}")
