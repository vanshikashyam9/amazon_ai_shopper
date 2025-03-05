from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging
from collections import defaultdict
import re

class ReviewAnalyzer:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def get_reviews(self, product_url, num_reviews=20):
        """Fetch and analyze product reviews"""
        try:
            # Navigate to reviews page
            reviews_url = product_url.replace('/dp/', '/product-reviews/')
            self.driver.get(reviews_url)
            time.sleep(2)  # Respectful delay

            reviews = []
            pages_scraped = 0
            reviews_collected = 0

            while reviews_collected < num_reviews and pages_scraped < 3:
                # Get reviews on current page
                page_reviews = self._extract_page_reviews()
                reviews.extend(page_reviews)
                reviews_collected += len(page_reviews)
                pages_scraped += 1

                # Try to go to next page if we need more reviews
                if reviews_collected < num_reviews:
                    if not self._go_to_next_page():
                        break

            return reviews[:num_reviews]

        except Exception as e:
            self.logger.error(f"Error fetching reviews: {str(e)}")
            return []

    def _extract_page_reviews(self):
        """Extract reviews from current page"""
        reviews = []
        try:
            review_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-hook='review']")
                )
            )

            for review in review_elements:
                try:
                    # Extract review details
                    review_data = {
                        'rating': self._extract_rating(review),
                        'title': self._get_element_text(review, "a[data-hook='review-title']"),
                        'text': self._get_element_text(review, "span[data-hook='review-body']"),
                        'date': self._get_element_text(review, "span[data-hook='review-date']"),
                        'verified': self._is_verified_purchase(review)
                    }
                    reviews.append(review_data)

                except Exception as e:
                    self.logger.error(f"Error extracting review details: {str(e)}")
                    continue

            return reviews

        except TimeoutException:
            self.logger.error("Timeout waiting for reviews")
            return []

    def analyze_reviews(self, reviews):
        """Analyze collected reviews and provide insights"""
        if not reviews:
            return None

        analysis = {
            'total_reviews': len(reviews),
            'average_rating': 0,
            'verified_purchases': 0,
            'rating_distribution': defaultdict(int),
            'common_phrases': self._extract_common_phrases(reviews),
            'sentiment_summary': {
                'positive': 0,
                'negative': 0,
                'neutral': 0
            }
        }

        # Analyze each review
        for review in reviews:
            # Update rating distribution
            rating = float(review['rating'])
            analysis['rating_distribution'][rating] += 1
            analysis['average_rating'] += rating

            # Count verified purchases
            if review['verified']:
                analysis['verified_purchases'] += 1

            # Basic sentiment analysis
            sentiment = self._analyze_sentiment(review['text'])
            analysis['sentiment_summary'][sentiment] += 1

        # Calculate average rating
        analysis['average_rating'] /= len(reviews)

        return analysis

    def _extract_rating(self, review_element):
        """Extract rating from review"""
        try:
            rating_string = review_element.find_element(
                By.CSS_SELECTOR, "i[data-hook='review-star-rating']"
            ).get_attribute("innerHTML")
            return float(re.search(r'(\d+(\.\d+)?)', rating_string).group(1))
        except:
            return 0.0

    def _is_verified_purchase(self, review_element):
        """Check if review is from verified purchase"""
        try:
            verified_text = review_element.find_element(
                By.CSS_SELECTOR, "span[data-hook='avp-badge']"
            ).text
            return "Verified Purchase" in verified_text
        except:
            return False

    def _get_element_text(self, parent_element, selector):
        """Safely get element text"""
        try:
            element = parent_element.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except:
            return ""

    def _go_to_next_page(self):
        """Attempt to navigate to next page of reviews"""
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, "li.a-last a"
            )
            next_button.click()
            time.sleep(2)  # Respectful delay
            return True
        except:
            return False

    def _extract_common_phrases(self, reviews):
        """Extract commonly mentioned phrases from reviews"""
        text = ' '.join(review['text'].lower() for review in reviews)
        # This is a simple implementation - could be enhanced with NLP
        words = text.split()
        phrases = defaultdict(int)
        
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases[phrase] += 1

        return dict(sorted(phrases.items(), key=lambda x: x[1], reverse=True)[:5])

    def _analyze_sentiment(self, text):
        """Basic sentiment analysis"""
        # This is a simple implementation - could be enhanced with ML
        positive_words = {'great', 'good', 'excellent', 'amazing', 'love', 'perfect'}
        negative_words = {'bad', 'poor', 'terrible', 'horrible', 'hate', 'worst'}
        
        text = text.lower()
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
