# This file is currently not integrated into the app

import requests
import dotenv
import os

dotenv.load_dotenv()

serp_api_key = os.getenv("SERPAPI_API_KEY")

def get_google_lens_results(image_url):
    # Set up the API request parameters
    params = {
        'api_key': serp_api_key,
        'engine': 'google_lens',
        'url': image_url
    }

    # Send a GET request to SerpAPI with the image URL
    response = requests.get('https://serpapi.com/search', params=params)
    
    return response

response = get_google_lens_results("https://helensclosetpatterns.com/wp-content/uploads/2021/03/March-Dress-Swetha-01.jpg")

def get_purchasable_products(response):
    # Parse the results to extract visual matches
    visual_matches = response.json().get("visual_matches", [])

    # Filter for purchasable products
    purchasable_products = []
    for match in visual_matches:
        if match.get("price"):  # Assuming products with a price are purchasable
            product = {
                "title": match.get("title"),
                "link": match.get("link"),
                "price": match.get("price"),
                "source": match.get("source"),
                "thumbnail": match.get("thumbnail")
            }
            purchasable_products.append(product)
    
    return purchasable_products

def format_purchasable_products(products):
    """
    Format the list of purchasable products into a pretty string output.

    Args:
        products (list): A list of dictionaries containing product information.

    Returns:
        str: A formatted string with product details.
    """
    if not products:
        return "No purchasable products found."

    output = "Purchasable Products:\n\n"
    for i, product in enumerate(products, 1):
        output += f"{i}. {product['title']}\n"
        output += f"   Price: {product['price']}\n"
        output += f"   Source: {product['source']}\n"
        output += f"   Link: {product['link']}\n"
        output += f"   Thumbnail: {product['thumbnail']}\n\n"

    return output.strip()


# purchasable_products = get_purchasable_products(response)
# print(format_purchasable_products(purchasable_products))