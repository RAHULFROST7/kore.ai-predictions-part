from datetime import datetime
import pandas as pd
import random
from joblib import load

from Predictions.SalesModel import SalesPredictor
from Predictions.Find_Product_encodings import Find_Product_encodings
from Predictions.GenerateDate import GenerateDate

global product_name
global category_name

global user_input
global time_period
global metric

def predict_sales(data):
    
    model = load("./Predictions/Model/trained_model-class.joblib")
        
    predictions = model.predict(data)
        
    return predictions

def predict_product():
    
    global product_name
    global user_input
    global time_period
    
    predictor = Find_Product_encodings()
    # print(product_name,type(product_name))
    encoded_product_names , product_names_encodings = predictor.map_product_name(product_name)
    # print(encoded_product_names , product_names_encodings)
    product_index = predictor.find_product_index(user_input,product_names_encodings)
    # print(product_index)
    if product_index == []:
        product = product_names_encodings[0]
        product_encoding = encoded_product_names[0]
        # print(product,product_encoding)
    else:
        product = product_names_encodings[product_index[0]]
        product_encoding = encoded_product_names[product_index[0]]
        # print(product,product_encoding)
    category = predictor.get_category(product)[0]
    
    category_encoding = predictor.find_mapping(category)
    # print(category_encoding)
    date_range_generator = GenerateDate()
    result_df = date_range_generator.generate_date_df(time_period) #np
    
    result_df['Product Name'] = product_encoding
    result_df['Product Category'] = category_encoding
    
    def is_weekend(day, month, year):
        date_obj = datetime(year, month, day)
        return int(date_obj.weekday() in [5, 6])  # 5 = Saturday, 6 = Sunday

    # Check if each date in the DataFrame is a holiday (weekend in this example)
    result_df['Holiday'] = result_df.apply(lambda row: is_weekend(row['Day'], row['Month'], row['Year']), axis=1)
    temp = [random.randint(25, 35) for _ in range(len(result_df))]
    result_df['Temperature'] = temp
    fuel = [random.randint(90, 110) for _ in range(len(result_df))]
    result_df['Fuel Price'] = fuel
    
    # Reorder the columns in X_sample to match the training data
    result_df = result_df.reindex(columns=['Product Name', 'Product Category', 'Holiday', 'Temperature', 'Fuel Price', 'Day', 'Month', 'Year'])
    result = pd.DataFrame({})
    # modelclass = SalesPredictor()
    print("problem here")
    predictions = predict_sales(result_df)
    print("problem not here")
    result["Number of Items Sold"] = predictions[:, 0]
    result["Weekly Sales"] = predictions[:, 1]
    result["Number of Items Sold"] = result["Number of Items Sold"].astype(int)
    result["Weekly Sales"] = result["Weekly Sales"].astype(float)

    # print(result)
    # Assuming 'result' is the DataFrame containing the columns "Number of Items Sold" and "Weekly Sales"
    result["Date"] = pd.to_datetime(result_df[["Year", "Month", "Day"]])
    
    # Calculate the rolling average for the "Weekly Sales" column
    window_sizews = 8  
    # You can adjust this value to change the smoothing effect
    window_sizenos = 8
    result["Weekly Sales (Rolling Avg)"] = result["Weekly Sales"].rolling(window=window_sizews).mean()
    result["Number of Items Sold (Rolling Avg)"] = result["Number of Items Sold"].rolling(window=window_sizenos).mean()
    result = result.dropna(axis=0)
    result["Number of Items Sold (Rolling Avg)"] = result["Number of Items Sold (Rolling Avg)"].astype(int)
    weekly = result['Weekly Sales (Rolling Avg)'].tolist()
    # print(weekly)
    nousold = result['Number of Items Sold (Rolling Avg)'].tolist()
    # print(nousold)
    dates = result['Date'].tolist()
    # print(date)
    # weekly, nousold ,date = 1,2,3
    min_value = min(weekly)
    max_value = max(weekly)

    # Calculate the range of the values
    value_range = max_value - min_value

    # Scale the values to the range of 0 to 60
    scaled_weekly = [(value - min_value) / value_range * 57 + 2 for value in weekly]
    scaled_weekly = [round(value) for value in scaled_weekly]
    # simplified_dates = [dt.strftime('%-m/%-d/%y') for dt in dates]
    # simplified_dates = [date.replace("-", "/").lstrip("0").replace("/0", "/") for date in dates]
    simplified_dates = [f"{date.day}/{date.month}/{date.year % 100}" for date in dates]

    # Find the minimum and maximum values in the list
    min_value = min(nousold)
    max_value = max(nousold)

    # Calculate the range of the values
    range_value = max_value - min_value

    # Scale and round the values to the range of 2 to 59
    scaled_nousold = [(value - min_value) / range_value * 57 + 2 for value in nousold]
   
    return scaled_weekly, scaled_nousold ,simplified_dates ,result["Number of Items Sold"].tolist() ,result["Weekly Sales"].tolist()
    
def predict_category():
    return 0,0,0,0,0

def main(given_name ,t_per,met,u_ip):
    
    global product_name
    global category_name
    global user_input
    global time_period
    global metric
    
    user_input = u_ip
    time_period = t_per
    metric = met
    
    predictor = Find_Product_encodings()
    
    closest_match,score,belongs = predictor.check_valid_prod_cat(given_name)
    
    
    if belongs == "Product":
        
        product_name = closest_match
        print(product_name,score,belongs)
        # try:
        weekly,nousold,date,noussold_unscaled,weekly_unscaled = predict_product()
        prediction_results = {
                            "user_input":user_input,
                            "product_name": product_name,
                            "pred_results":
                                {
                                    "Weekly sales":weekly,
                                    "Weekly sales unscaled":weekly_unscaled,
                                    "No of units sold":nousold,
                                    "No of units sold unscaled":noussold_unscaled,
                                    "date":date
                                }
                        }
        return prediction_results
        # except:
        #     return {'error':"in predict"}
    elif belongs == "Category":
        
        category_name = closest_match
        print(category_name,score,belongs)
        weekly,nousold,date,noussold_unscaled,weekly_unscaled = predict_category()
        prediction_results = {
                            "user_input":user_input,
                            "product_name": category_name,
                            "pred_results":
                                {
                                    "Weekly sales":weekly,
                                    "Weekly sales unscaled":weekly_unscaled,
                                    "No of units sold":nousold,
                                    "No of units sold unscaled":noussold_unscaled,
                                    "date":date
                                }
                         }
        return prediction_results
         
    else:
        return {
            'error':'Recheck your product or category name'
        }
        

# if __name__ == "__main__":

#     print(main(u_ip = "what will be the sales of samrtphone next month",given_name = "smartphone",t_per="next month",met="Sales"))