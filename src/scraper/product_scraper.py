from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging

class ProductScraper:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def search_product(self, query):
        """Search for a product on Amazon"""
        try:
            # Find and fill the search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            search_box.clear()
            search_box.send_keys(query)
            
            # Click search button
            search_button = self.driver.find_element(By.ID, "nav-search-submit-button")
            search_button.click()
            
            # Wait for results to load
            time.sleep(2)  # Adding a small delay to be respectful to Amazon's servers
            
            return True
        except Exception as e:
            self.logger.error(f"Error searching for product: {str(e)}")
            return False

    def get_top_products(self, num_products=5):
        """Get details of top products from search results"""
        products = []
        try:
            # Wait for product listings
            product_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
                )
            )

            for product in product_list[:num_products]:
                try:
                    # Extract product details
                    title = product.find_element(
                        By.CSS_SELECTOR, "h2 a span"
                    ).text.strip()
                    
                    # Get price (handle different price formats)
                    try:
                        price = product.find_element(
                            By.CSS_SELECTOR, "span.a-price-whole"
                        ).text
                    except:
                        price = "Price not found"
                    
                    # Get rating
                    try:
                        rating = product.find_element(
                            By.CSS_SELECTOR, "span.a-icon-alt"
                        ).get_attribute("innerHTML")
                    except:
                        rating = "No rating"
                    
                    # Get number of reviews
                    try:
                        review_count = product.find_element(
                            By.CSS_SELECTOR, "span.a-size-base.s-underline-text"
                        ).text
                    except:
                        review_count = "0"

                    # Get product link
                    link = product.find_element(
                        By.CSS_SELECTOR, "h2 a"
                    ).get_attribute("href")

                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'review_count': review_count,
                        'link': link
                    })

                except Exception as e:
                    self.logger.error(f"Error extracting product details: {str(e)}")
                    continue

            return products

        except TimeoutException:
            self.logger.error("Timeout waiting for product listings")
            return []
        except Exception as e:
            self.logger.error(f"Error getting top products: {str(e)}")
            return []

    def analyze_product(self, product_url):
        """Navigate to product page and analyze details"""
        try:
            self.driver.get(product_url)
            time.sleep(2)  # Respectful delay

            # Get detailed product information
            product_info = {
                'title': self.get_element_text(By.ID, "productTitle"),
                'price': self.get_element_text(By.CSS_SELECTOR, "span.a-price-whole"),
                'rating': self.get_element_text(By.CSS_SELECTOR, "span.a-icon-alt"),
                'features': self.get_product_features(),
                'availability': self.get_element_text(By.ID, "availability"),
            }

            return product_info

        except Exception as e:
            self.logger.error(f"Error analyzing product: {str(e)}")
            return None

    def get_element_text(self, by, selector):
        """Safely get element text"""
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((by, selector))
            )
            return element.text.strip()
        except:
            return None

    def get_product_features(self):
        """Get product feature bullets"""
        try:
            feature_list = self.driver.find_elements(
                By.CSS_SELECTOR, "#feature-bullets ul li span"
            )
            return [feature.text.strip() for feature in feature_list]
        except:
            return []
