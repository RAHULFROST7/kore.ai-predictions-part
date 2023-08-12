from flask import Flask, request, jsonify
from flask import render_template
from main import main
import subprocess
# import json
from Analysis.Analyzer_p1 import SalesAnalyzer
import sys
import os

app = Flask(__name__)

global data_json
data_json={}
global prediction_result
prediction_result = {}
global install_count
install_count = 0

def install_packages():
    # Package name to install
    package_name = "xgboost"

    # Use subprocess to run pip install command
    try:
        subprocess.check_call(["pip", "install", package_name])
        print(f"Package '{package_name}' installed successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to install package '{package_name}'.")
        
@app.route('/predict', methods=['POST'])
def predict():
    global install_count
    if install_count == 0:
        install_packages()
    install_count = 1
    global prediction_result
    try:
        # Access the data sent in the request body
        data = request.json

        # Extract the variables from the data dictionary
        user_input = data.get('user_input')
        product_name = data.get('product_name')
        time_period = data.get('time_period')
        metric = data.get('metric')

        # Call the predict_sales function to get the prediction result
        prediction_result = main(given_name = product_name,t_per=time_period,u_ip = user_input,met=metric)

        # Return the prediction result as a JSON response
        return jsonify(prediction_result)

    except Exception as e:
        # Handle any exceptions and return an error response if needed
        return jsonify({"error": str(e)}), 400
    
    
    
@app.route('/predictions_report')
def pred_report():
    
    global prediction_result
    # print(data_json)
    if prediction_result != {}:
        return render_template('predictions_report.html', data=prediction_result)
    else:
        return jsonify({"error": str("Make some predictions first")}), 400 
    
@app.route('/predictions_link', methods=['GET'])
def predict_get():
    try:
        prediction_result = {
            "link":"https://9308-103-163-248-170.ngrok-free.app/predictions_report"
        }

        # Return the prediction result as a JSON response
        return prediction_result

    except Exception as e:
        # Handle any exceptions and return an error response if needed
        return jsonify({"error": str(e)}), 400
    
    
@app.route('/analyze', methods=['POST'])
def analysis():
    global data_json
    try:
        # Access the data sent in the request body
        data = request.json
        product_name = data.get('product_name')
        metric = data.get('metric')
        
        # Define the paths for data CSV and product mapping JSON
        # data_csv_path = r"E:\Projects and codes\Kore-ai_flask_ml-for-sales-prediction\Data\finaldata_1.0.csv"
        # product_mapping_path = r"E:\Projects and codes\Kore-ai_flask_ml-for-sales-prediction\Data\product_names.json"
        data_csv_path = "./Data/finaldata_1.0.csv"
        product_mapping_path = "./Data/product_names.json"
        # './Data/test.txt'

        # Create an instance of the SalesAnalyzer class
        sales_analyzer = SalesAnalyzer(data_csv_path, product_mapping_path)

        # Perform sales analysis based on the provided input and metrics
        results = sales_analyzer.analyze_sales_p1(product_name)
        if results is not None and results != 404:
            data_top_selling = results['top-selling products']
            data_total_sales_per_product = results['total sales per product']
            data_items_sold_per_product = results['items sold per product']

            # Extract the required information and create data_json
            data_json = {
                'Product Name' : list(set(data_top_selling['Product Name'].tolist())),
                'Number of Items Sold' : list(set(data_top_selling['Number of Items Sold'].tolist())),
                'Total Sales' : data_total_sales_per_product['Weekly Sales'].tolist(),
                'Items Sold per Product' : data_items_sold_per_product['Number of Items Sold'].tolist(),
            }
            unique_names = list(set(data_json['Product Name']))
            data_json['unique names'] = unique_names
            print(data_json)
            return jsonify(data_json)
        else:
            data_json = {
                "error" : f"Cant find a match for this product '{product_name}' "
            }
            print(data_json)
            return jsonify(data_json),404

    except Exception as e:
        # Handle any exceptions and return an error response if needed
        return jsonify({"error": str(e)}), 400 
    
@app.route('/analysis_report')
def analysis_report():
    
    global data_json
    print(data_json)
    
    if data_json != {}:
        return render_template('analysis_report.html', data=data_json)
    else:
        return jsonify({"error": str("First make some analysis")}), 400 
    
@app.route('/analysis_link', methods=['GET'])
def analysis_get():
    try:
        analysis_result = {
            "link":"https://9308-103-163-248-170.ngrok-free.app/analysis_report"
        }

        # Return the analysis result as a JSON response
        return analysis_result

    except Exception as e:
        # Handle any exceptions and return an error response if needed
        return jsonify({"error": str(e)}), 400
    
@app.route('/restart')
def restart():
    restart_server()
    return "Restart succesfull"

def restart_server():
    print("Restarting Flask server...")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
if __name__ == "__main__":
    app.run(debug=True,port=8000)
