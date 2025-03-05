# Amazon AI Shopper

An intelligent shopping assistant that uses AI to analyze Amazon products and reviews, helping you make better purchasing decisions.

## Overview

Amazon AI Shopper automates the process of researching products on Amazon by:
- Searching for products based on your queries
- Analyzing top search results
- Extracting key product details and features
- Collecting and analyzing customer reviews
- Using OpenAI to provide personalized purchase recommendations

## Features

- **Automated Amazon Search**: Search for products without manual browsing
- **Smart Product Analysis**: Compare multiple products objectively
- **Review Sentiment Analysis**: Process customer reviews to identify key insights
- **Budget Filtering**: Only show products within your price range
- **AI-Powered Recommendations**: Get personalized advice using OpenAI
- **Cookie-Based Authentication**: Secure and reliable Amazon login

## Requirements

- Python 3.8+
- Chrome browser
- Internet connection
- Amazon account
- OpenAI API key

## Quick Start

1. **Setup and Installation**:
   ```bash
   # Clone the repository (or download it)
   git clone https://github.com/yourusername/amazon_ai_shopper.git
   cd amazon_ai_shopper

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install selenium python-dotenv openai beautifulsoup4 pandas
   ```

2. **Configure Credentials**:
   - Create `config/config.env` with your credentials:
     ```
     AMAZON_EMAIL=your_amazon_email@example.com
     AMAZON_PASSWORD=your_amazon_password
     OPENAI_API_KEY=your_openai_api_key
     ```

3. **Run the Program**:
   ```bash
   python -m src.main
   ```

## Detailed Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/amazon_ai_shopper.git
   cd amazon_ai_shopper
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install selenium python-dotenv openai beautifulsoup4 pandas
   ```

4. Create a requirements.txt file (optional):
   ```bash
   pip freeze > requirements.txt
   ```

## Configuration

1. Create a `config.env` file in the `config` directory:
   ```
   AMAZON_EMAIL=your_amazon_email@example.com
   AMAZON_PASSWORD=your_amazon_password
   OPENAI_API_KEY=your_openai_api_key
   ```

2. Ensure your Amazon account is set up with:
   - Valid login credentials
   - A default shipping address
   - A default payment method (if you plan to use the purchase feature)

## Usage

Run the main script from the project root:
```bash
python -m src.main
```

Follow the interactive prompts:
1. Enter what you want to buy
2. Specify your budget (enter 0 for no budget limit)
3. Wait while the program searches and analyzes products
4. Review the AI-generated recommendation
5. Choose whether to purchase the recommended item

### Example Interaction

```
What would you like to buy? wireless headphones
What's your budget? 200

Searching for 'wireless headphones'...
Analyzing top products...
Collecting review data...
Generating AI recommendation...

AI Recommendation:
1. Recommended Product: Sony WH-1000XM4 Wireless Headphones
2. Reasoning: The Sony WH-1000XM4 offers the best balance of sound quality, noise cancellation, and battery life among the analyzed products. While it's at the higher end of your budget, the overwhelmingly positive reviews and premium features justify the price.
3. Key Pros:
   - Industry-leading noise cancellation
   - 30-hour battery life
   - Comfortable for extended wear
   - High sound quality with LDAC support
4. Key Cons:
   - Higher price point
   - Can only connect to one device at a time
5. Price: $198.00

Would you like to purchase this item? (yes/no) 
```

## Project Structure

amazon_ai_shopper/
├── config/
│ └── config.env # Configuration settings
├── src/
│ ├── auth/
│ │ └── amazon_auth.py # Amazon authentication
│ ├── scraper/
│ │ └── product_scraper.py # Product data extraction
│ ├── analyzer/
│ │ └── review_analyzer.py # Review analysis
│ └── main.py # Main application
├── venv/ # Virtual environment
├── amazon_cookies.json # Saved session cookies
└── README.md # This file    

## How It Works

### Authentication
The system uses Selenium to automate Chrome browser interactions. It handles Amazon login using your credentials and maintains session cookies to avoid repeated logins.

### Product Analysis
The program searches Amazon based on your query, collects detailed information about top products, and analyzes the following aspects:
- Product features and specifications
- Price vs. competitive products
- Average customer rating and review count
- Review sentiment analysis

### AI Recommendation
Using OpenAI's GPT models, the system:
1. Analyzes all collected product data
2. Evaluates price-to-quality ratio
3. Considers customer sentiment from reviews
4. Generates a personalized recommendation

## Security Considerations

- **Credentials**: Your Amazon and OpenAI credentials are stored locally in the config file. Never share this file.
- **Cookies**: Login session cookies are saved to disk for convenience. Delete the cookie file if using a shared computer.
- **Automated Access**: The program uses techniques to appear as a regular user, but automated access to Amazon may violate their Terms of Service.


## License

This project is licensed under the MIT License. See the LICENSE file for details.