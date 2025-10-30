import os
import sys


import pandas as pd
import pickle
import numpy as np
from src.exception import CustomException

from sklearn.metrics import r2_score

def save_object(file_path:str,obj:object)->None:
    '''
    This function is used to save the object in the file path
    '''
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)


def evaluate_models(X_train,y_train,X_test,y_test,models:dict)->dict:
    '''
    This function is used to evaluate the models and return the report
    '''
    try:
        report={}

        for i in range(len(models)):
            model=list(models.values())[i]
            # Train the model
            model.fit(X_train,y_train)

            # Get the predictions for train and test data
            y_train_pred=model.predict(X_train)
            
            # Get the predictions for test data
            y_test_pred=model.predict(X_test)
            # Calculate r2 score for train and test data
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            #report[list(models.keys())[i]]={"train_score":train_model_score,"test_score":test_model_score}

            report[list(models.keys())[i]]=test_model_score

        return report

    except Exception as e:
        raise CustomException(e,sys)