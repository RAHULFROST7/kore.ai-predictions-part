from joblib import load

class SalesPredictor:
    def __init__(self):
        self.model = None

    def predict_sales(self,data):
        
        self.model = load("./Predictions/Model/trained_model-class.joblib")
        
        predictions = self.model.predict(data)
        
        return predictions
        # return self.model


# obj = SalesPredictor()
# model = obj.predict(data=None)
# print(model)