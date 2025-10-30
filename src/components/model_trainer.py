import os
import sys

from src.logger import logging
from src.exception import CustomException


from dataclasses import dataclass

from catboost import CatBoostRegressor

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor

from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path =   os.path.join("artifacts","model.pkl")

class ModelTrainer:

    # constructor
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    # Initiate model trainer for different algorithms and select best model
    def initiate_model_trainer(self,train_array,test_array):
        
        try:
            # Split the data into features and target variable
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1], # all rows, all columns except last(output column)
                train_array[:,-1], # all rows, only last column(output column)
                test_array[:,:-1], # all rows, all columns except last(output column)
                test_array[:,-1] # all rows, only last column(output column)
            )
            # Define different models to train
            models={
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "XGB Regressor":XGBRegressor(),
                "CatBoost Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor":AdaBoostRegressor(),
                "KNeighbors Regressor":KNeighborsRegressor()
            }
            # Evaluate all models and get the report
            model_report:dict= evaluate_models(X_train,y_train,X_test,y_test,models)
            # Get the best model score from the report

            best_model_score = max(sorted(model_report.values()))

            # Get the best model name from the report
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            # Get the best model object
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                logging.info("No best model found on both training and testing data")
                raise CustomException("No best model found")

            logging.info(f"Best model found ,model name:{best_model_name},R2 score:{best_model_score}")

            # Save the best model to the file for future use
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            # Predict the test data using best model
            predicted=best_model.predict(X_test)
            r2_square = r2_score(y_test,predicted)
            return r2_square

        except Exception as e:
            logging.info("Exception occurred at model training")
            raise CustomException(e,sys)