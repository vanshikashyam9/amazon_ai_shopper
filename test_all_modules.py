import os
import sys

def test_imports():
    try:
        # Test auth module
        from src.auth.amazon_auth import AmazonAuthenticator
        print("✅ Authentication module imported successfully")
        
        # Test scraper module
        from src.scraper.product_scraper import ProductScraper
        print("✅ Product scraper module imported successfully")
        
        # Test analyzer module
        from src.analyzer.review_analyzer import ReviewAnalyzer
        print("✅ Review analyzer module imported successfully")
        
        # Test main module
        from src.main import AmazonAIShopperBot
        print("✅ Main module imported successfully")
        
        # Check environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv('config/config.env')
            
            amazon_email = os.getenv('AMAZON_EMAIL')
            amazon_password = os.getenv('AMAZON_PASSWORD')
            openai_api_key = os.getenv('OPENAI_API_KEY')
            
            if amazon_email and amazon_password and openai_api_key:
                print("✅ Environment variables loaded successfully")
            else:
                missing = []
                if not amazon_email: missing.append('AMAZON_EMAIL')
                if not amazon_password: missing.append('AMAZON_PASSWORD')
                if not openai_api_key: missing.append('OPENAI_API_KEY')
                print(f"❌ Missing environment variables: {', '.join(missing)}")
        
        except Exception as e:
            print(f"❌ Error loading environment variables: {str(e)}")
        
        print("\nAll modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error importing modules: {str(e)}")
        return False

if __name__ == "__main__":
    test_imports()
