import os
import sys

import pandas as pd
import pickle
import numpy as np
from src.exception import CustomException

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


