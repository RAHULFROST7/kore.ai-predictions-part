from fuzzywuzzy import process
import pandas as pd
import json


class SalesAnalyzer:
    def __init__(self, data_csv_path, product_mapping_path):
        # Sample data
        self.data = pd.read_csv(data_csv_path)

        # Product and category mappings
        with open(product_mapping_path) as file:
            self.product_category_mapping = json.load(file)

        # Create a DataFrame
        self.df = pd.DataFrame(self.data)
        self.error_code = 404
    # Function to calculate sales performance
    def calculate_sales_performance(self, data):
        return data["Weekly Sales"].sum()

    # Function to calculate top-selling products
    def calculate_top_selling_products(self, data):
        return data.sort_values("Number of Items Sold", ascending=False)[["Product Name", "Number of Items Sold"]]

    # Function to calculate total sales for each product
    def calculate_total_sales_per_product(self, data):
        return data.groupby("Product Name")["Weekly Sales"].sum().reset_index()

    # Function to calculate number of items sold for each product
    def calculate_items_sold_per_product(self, data):
        return data.groupby("Product Name")["Number of Items Sold"].sum().reset_index()

    # Function to perform fuzzy string matching to find the most similar product name
    def find_closest_match(self, user_input, choices):
        closest_match, score = process.extractOne(user_input, choices)
        return closest_match, score

    # Function to map the matched product to the correct category using the provided JSON file
    def map_product_to_category(self, matched_product):
        for category, products in self.product_category_mapping.items():
            if matched_product in products:
                return category
        return None

    # Function to perform sales analysis based on the provided input (product name or category) and metrics
    def analyze_sales_p1(self, user_input):
        # Find the closest product or category match using fuzzy string matching
        closest_match, score = self.find_closest_match(user_input, self.df['Product Name'].unique())
        
        if score < 65:
            closest_category, category_score = self.find_closest_match(user_input, self.df['Product Category'].unique())
            print(f"Matched category: {closest_category} score:{category_score}")
            
            if category_score < 60:
                
                print(f"No matching product or category found for input: {user_input}")
                
                return self.error_code
                # return self.error_code
            else:
                if user_input in self.df['Product Category'].values:
                    # User provided an exact product name
                    filtered_data = self.df[self.df['Product Category'] == user_input]
                else:
                # Filter the data based on the closest category match
                    filtered_data = self.df[self.df['Product Category'] == closest_category]
                    
                results = {
                "top-selling products": self.calculate_top_selling_products(filtered_data),
                "total sales per product": self.calculate_total_sales_per_product(filtered_data),
                "items sold per product": self.calculate_items_sold_per_product(filtered_data),
                }

            return results

        else:
            closest_category = self.map_product_to_category(closest_match)

            if closest_category is None:
                print(f"No matching category found for product: {closest_match}")
                return self.error_code

            print(f"Matched product: {closest_match}, score : {score}, Matched category: {closest_category}")

            if user_input in self.df['Product Name'].values:
                # User provided an exact product name
                filtered_data = self.df[self.df['Product Name'] == user_input]
            else:
                # Filter the data based on the closest category match
                filtered_data = self.df[self.df['Product Category'] == closest_category]

            results = {
                "top-selling products": self.calculate_top_selling_products(filtered_data),
                "total sales per product": self.calculate_total_sales_per_product(filtered_data),
                "items sold per product": self.calculate_items_sold_per_product(filtered_data),
            }

            return results
    