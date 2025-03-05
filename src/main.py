import logging
import os
import json
import time
from dotenv import load_dotenv
import openai
from src.auth.amazon_auth import AmazonAuthenticator
from src.scraper.product_scraper import ProductScraper
from src.analyzer.review_analyzer import ReviewAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AmazonAIShopperBot:
    def __init__(self):
        # Load environment variables
        load_dotenv('config/config.env')
        
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize components
        self.auth = AmazonAuthenticator()
        self.driver = None
        self.scraper = None
        self.analyzer = None

    def start(self):
        """Initialize the bot"""
        try:
            self.auth.initialize_driver()
            self.driver = self.auth.driver
            
            if not self.auth.login():
                raise Exception("Failed to login to Amazon")

            self.scraper = ProductScraper(self.driver)
            self.analyzer = ReviewAnalyzer(self.driver)
            
            logger.info("Bot initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize bot: {str(e)}")
            return False

    def search_and_analyze(self, product_query, budget=None):
        """Search for products and analyze them"""
        try:
            # Search for the product
            if not self.scraper.search_product(product_query):
                raise Exception("Failed to search for product")

            # Get top products
            products = self.scraper.get_top_products(num_products=5)
            if not products:
                raise Exception("No products found")

            analyzed_products = []
            
            for product in products:
                # Skip if price is above budget
                if budget and self._extract_price(product['price']) > budget:
                    continue

                # Get detailed product info
                product_info = self.scraper.analyze_product(product['link'])
                if not product_info:
                    continue

                # Get and analyze reviews
                reviews = self.analyzer.get_reviews(product['link'], num_reviews=20)
                review_analysis = self.analyzer.analyze_reviews(reviews)

                analyzed_products.append({
                    'basic_info': product,
                    'detailed_info': product_info,
                    'review_analysis': review_analysis
                })

            # Use AI to make a recommendation
            recommendation = self._get_ai_recommendation(analyzed_products, product_query)
            
            return recommendation

        except Exception as e:
            logger.error(f"Error in search and analysis: {str(e)}")
            return None

    def _extract_price(self, price_str):
        """Extract numerical price from string"""
        try:
            return float(''.join(filter(str.isdigit, price_str)))
        except:
            return float('inf')

    def _get_ai_recommendation(self, products, query):
        """Get AI recommendation using OpenAI"""
        try:
            # Prepare the prompt
            prompt = f"""
            I'm looking to buy {query}. Based on the following product data, please recommend the best option:
            
            {json.dumps(products, indent=2)}
            
            Please consider:
            1. Price-to-quality ratio
            2. Review sentiment and verified purchase ratio
            3. Average rating and number of reviews
            4. Key features and their relevance
            
            Provide your recommendation in this format:
            1. Recommended Product: [product name]
            2. Reasoning: [detailed explanation]
            3. Key Pros: [list of main advantages]
            4. Key Cons: [list of main disadvantages]
            5. Price: [price]
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI shopping assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error getting AI recommendation: {str(e)}")
            return None

    def purchase_product(self, product_url):
        """Purchase the recommended product"""
        # TODO: Implement purchase functionality
        logger.info(f"Attempting to purchase product: {product_url}")
        logger.warning("Purchase functionality not yet implemented")
        
        # For a real implementation, this would handle:
        # 1. Add to cart
        # 2. Proceed to checkout
        # 3. Confirm shipping address
        # 4. Select payment method
        # 5. Place order
        
        return False

    def close(self):
        """Clean up resources"""
        if self.auth:
            self.auth.close()
            logger.info("Browser closed")

def main():
    # Create the bot
    bot = AmazonAIShopperBot()
    
    try:
        # Start the bot
        if bot.start():
            # Get user input
            query = input("What would you like to buy? ")
            budget_input = input("What's your budget? (Enter 0 for no budget) ")
            budget = float(budget_input) if budget_input and float(budget_input) > 0 else None
            
            # Search and analyze
            print(f"\nSearching for '{query}'...")
            recommendation = bot.search_and_analyze(query, budget)
            
            if recommendation:
                print("\nAI Recommendation:")
                print(recommendation)
                
                # Ask if user wants to purchase
                purchase = input("\nWould you like to purchase this item? (yes/no) ").lower()
                if purchase == 'yes':
                    # Extract product URL from recommendation (simplified)
                    # In a real implementation, parse the recommendation to get the URL
                    print("Purchase functionality is currently disabled for safety")
            else:
                print("Sorry, couldn't find a suitable recommendation.")
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    
    finally:
        # Always close the browser
        bot.close()

if __name__ == "__main__":
    main()
