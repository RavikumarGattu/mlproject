import sys

# Function to get detailed error message
def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filename=exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(filename,exc_tb.tb_lineno,str(error))
    return error_message

# Custom Exception class
class CustomException(Exception):
    # Constructor of the class
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail)
    # String representation of the error
    def __str__(self):
        return self.error_message

