
from fuzzywuzzy import process
import pickle
import json
import re

class Find_Product_encodings:
    def __init__(self):
        self.path_mapings = "./Data/mappings.pickle" 
        self.config_path  = "./Data/config.toml"
        self.product_josn_path = "./Data/product_names.json"
        
    def check_valid_prod_cat(self,name):
        with open(self.product_josn_path,'r') as file :
            products = json.load(file)      
        closest_match = None
        max_score = 0
        is_product = False
        is_cat = False
        for category, products in products.items():
            # Check similarity with the category
            category_score = process.extractOne(name, [category])[1]
            if category_score > max_score and category_score > 70:
                max_score = category_score
                closest_match = category
                is_cat = True

            # Check similarity with each product in the category
            for product in products:
                product_score = process.extractOne(name, [product])[1]
                if product_score > max_score and product_score > 70:
                    max_score = product_score
                    closest_match = product
                    is_product = True

        return closest_match, max_score, "Product" if is_product else "Category" if is_cat else None


    def get_category(self,product_name):
        with open(self.product_josn_path, 'r') as f:
            product_names = json.load(f)
        categories = []
        for category, products in product_names.items():
            for product in products:
                if re.search(r"(?i)\b{}\b".format(product_name), product.lower()):
                    categories.append(category)
        return categories
    
    def find_mapping(self,category):
        
        for key, value in self.product_category_mappings.items():
            if category.lower() == value.lower():
                return key
        return None

    def load_mappings(self):
        with open(self.path_mapings, "rb") as file:
            mappings = pickle.load(file)
        # print(mappings)
        if mappings is None:
            raise FileNotFoundError("Mappings file not found")
        
        self.product_name_mappings = mappings["product_name_mappings"]
        self.product_category_mappings = mappings["product_category_mappings"]
        self.holiday_mappings = mappings["holiday_mappings"]


    def map_product_name(self, product_name):
        self.load_mappings()
        matching_mappings = []
        matching_names = []

        # Check if the product_name is a substring of any product in the mappings
        for code, name in self.product_name_mappings.items():
            if product_name.lower() in name.lower():
                matching_mappings.append(code)
                matching_names.append(name)

        return matching_mappings, matching_names

    def find_product_index(self,sentence, prod_name_list):
        # Convert the sentence and product names to lowercase for case-insensitive matching
        sentence_lower = sentence.lower()
        prod_name_list_lower = [name.lower() for name in prod_name_list]

        # Search for the product name in the sentence
        found_product_indices = [i for i, name in enumerate(prod_name_list_lower) if name in sentence_lower]

        return found_product_indices
