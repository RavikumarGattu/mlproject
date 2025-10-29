import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils import save_object
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:

    '''

    
    This class is responsible for data transformation

    '''


    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
     
    #Creating the data transformation object
    def get_data_transformer_object(self):
        try:
            logging.info("Data Transformation initiated")
            numerical_columns=['writing_score','reading_score']
            categorical_columns=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
            #Numerical Pipeline
            numerical_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ])
            logging.info("Numerical pipelines created successfully")
            
            #Categorical Pipeline
            categorical_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('onehot',OneHotEncoder(handle_unknown='ignore'))
            ])
            logging.info("Categorical pipelines created successfully")
           
            #Combining both pipelines
            preprocessor=ColumnTransformer(
                transformers=[
                    ('num_pipeline',numerical_pipeline,numerical_columns),
                    ('cat_pipeline',categorical_pipeline,categorical_columns)
                ]
            )
            logging.info("Data Transformation completed")
            return preprocessor
        except Exception as e:
            logging.error("Error occurred during Data Transformation")
            raise CustomException(e,sys) from e
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            #Reading the train and test data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read train and test data completed")
            #logging.info(f"Train Dataframe Head : \n{train_df.head().to_string()}")
            #logging.info(f"Test Dataframe Head : \n{test_df.head().to_string()}")

            logging.info("Obtaining preprocessor object")
            preprocessor_obj=self.get_data_transformer_object()

            target_column_name='math_score'
            numerical_columns=['writing_score','reading_score']

            #Splitting the data into input and target features
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            #Transforming using preprocessor object
            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing dataframes.")

            # Combining input features and target variable
            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object.")

            #Saving the preprocessing object
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            logging.error("Error occurred during initiate_data_transformation")
            raise CustomException(e,sys) from e

    