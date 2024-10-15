import os
import dotenv
from langchain_core.tools import tool
from langchain_community.tools.google_lens import GoogleLensQueryRun
from langchain_community.utilities.google_lens import GoogleLensAPIWrapper
from typing import List, Dict

dotenv.load_dotenv()

google_lens_tool = GoogleLensQueryRun(api_wrapper=GoogleLensAPIWrapper())

@tool
def find_similar_products(image_url: str) -> List[Dict[str, str]]:
    """Finds similar products to the image uploaded by the user.

    This tool should be used when:
    1. A user has uploaded an image of a clothing item or outfit.
    2. You need to find similar products available for purchase.
    3. You want to provide shopping options based on the user's style preferences.

    Args:
        image_path: A string representing the path to the uploaded image file.

    Returns:
        A list of dictionaries containing information about similar products found.
        Each dictionary includes keys like 'title', 'link', 'price', 'source', and 'thumbnail'.

    Raises:
        ValueError: If the image path is invalid or no similar products are found.
    """
    try:
        # Use the existing Google Lens tool to find similar products
        similar_products = find_purchasable_products_with_google_lens(image_url)
        
        if not similar_products:
            return "No similar products found for the uploaded image."
        
        return similar_products
    except Exception as e:
        return f"Error finding similar products: {str(e)}"

@tool
def find_purchasable_products_with_google_lens(image_url: str) -> List[Dict[str, str]]:
    """Analyzes an image using Google Lens and returns purchasable products.

    Args:
        image_url: A string representing the URL of the image to be analyzed.

    Returns:
        A list of dictionaries containing information about purchasable products found in the image.
        Each dictionary includes keys like 'title', 'link', 'price', 'source', and 'thumbnail'.

    Raises:
        ValueError: If the image URL is invalid or the analysis fails.
    """
    try:
        results = google_lens_tool.run(image_url)
        
        # Parse the results to extract visual matches
        visual_matches = results.get("visual_matches", [])
        
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
    except Exception as e:
        raise ValueError(f"Error analyzing image or finding purchasable products: {str(e)}")



@tool
def process_uploaded_file(file_path: str) -> str:
    """
    Processes the uploaded file and performs the necessary operations.

    Args:
        file_path: A string representing the path to the uploaded file.

    Returns:
        A string indicating the result of the file processing.
    """
    if not file_path:
        return "No file uploaded. Please upload a file to proceed."

    # Additional file validation can be added here
    if not os.path.exists(file_path):
        return "Uploaded file not found. Please check the file path."

    try:
        # Perform the tool's main logic here
        result = perform_file_processing(file_path)
        return f"File processed successfully: {result}"
    except Exception as e:
        return f"Error processing file: {str(e)}"

def perform_file_processing(file_path: str) -> str:
    # Placeholder for the actual file processing logic
    return "File content processed"

@tool
def extract_image_information(image_path: str) -> str:
    """
    Extracts detailed information about a dress or product based on the provided image.

    This tool should be used when:
    1. A user uploads or provides an image of a clothing item or outfit.
    2. Detailed analysis of the clothing item's characteristics is required.
    3. The conversation involves discussing specific attributes of a garment.
    4. Recommendations based on the item's style, pattern, or description are needed.
    5. Comparing the item to other clothing pieces or styles is necessary.

    Args:
        image_path: A string representing the path to the image file.

    Returns:
        A string containing detailed information about the product in the image,
        including outfit description, pattern type, and style.
    """
    try:
        image_info = get_image_information(image_path)
        
        return f"""Product Information:
        Outfit Description: {image_info['outfit_description']}
        Pattern Type: {image_info['outfit_pattern_type']}
        Style: {image_info['outfit_style']}"""
    except Exception as e:
        return f"Error processing image: {str(e)}"



# Example usage:
# products = find_purchasable_products_with_google_lens("https://i.imgur.com/HBrB8p0.png")
# for product in products:
#     print(f"Title: {product['title']}")
#     print(f"Price: {product['price']}")
#     print(f"Link: {product['link']}")
#     print("---")

# from typing import List, Dict
# import random

# @tool
# def get_personalized_fashion_advice(
#     style_preferences: List[str],
#     body_type: str,
#     occasion: str,
#     budget: str,
#     current_trends: List[str] = None
# ) -> Dict[str, str]:
#     """
#     Provides personalized fashion advice based on user preferences and current trends.

#     Args:
#         style_preferences: List of preferred styles (e.g., ["casual", "bohemian", "vintage"])
#         body_type: User's body type (e.g., "hourglass", "pear", "athletic")
#         occasion: The event or setting for the outfit (e.g., "work", "date night", "wedding")
#         budget: Price range for the outfit (e.g., "low", "medium", "high")
#         current_trends: Optional list of current fashion trends

#     Returns:
#         A dictionary containing outfit recommendations and styling tips
#     """
#     # Simulated fashion database (in a real scenario, this would be a more comprehensive system)
#     fashion_items = {
#         "tops": ["blouse", "t-shirt", "sweater", "cardigan"],
#         "bottoms": ["jeans", "skirt", "trousers", "shorts"],
#         "dresses": ["maxi dress", "cocktail dress", "shift dress", "wrap dress"],
#         "shoes": ["sneakers", "heels", "flats", "boots"],
#         "accessories": ["necklace", "earrings", "scarf", "belt"]
#     }

#     # Simple logic to select items (in a real scenario, this would be more sophisticated)
#     top = random.choice(fashion_items["tops"])
#     bottom = random.choice(fashion_items["bottoms"])
#     shoes = random.choice(fashion_items["shoes"])
#     accessory = random.choice(fashion_items["accessories"])

#     # Adjust selections based on occasion
#     if occasion.lower() == "wedding":
#         outfit = random.choice(fashion_items["dresses"])
#     else:
#         outfit = f"{top} with {bottom}"

#     # Generate styling tips
#     styling_tips = [
#         f"Consider your {body_type} body type when choosing fit",
#         f"Accessorize with a {accessory} to complete the look",
#         "Don't be afraid to mix and match patterns",
#         f"Choose {shoes} that complement your outfit and are appropriate for the {occasion}"
#     ]

#     # Incorporate current trends if provided
#     if current_trends:
#         trend_tip = f"Incorporate the '{random.choice(current_trends)}' trend into your outfit"
#         styling_tips.append(trend_tip)

#     return {
#         "outfit_recommendation": outfit,
#         "shoes": shoes,
#         "accessory": accessory,
#         "styling_tips": styling_tips
#     }
