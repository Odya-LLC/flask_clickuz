class ClickUz_Errors():
    
    def __init__(self):
        self.errors = {
            "0" : "Success",
            "-1" : "SIGN CHECK FAILED!",
            "-2" : "Incorrect parameter amount",
            "-3" : "Action not found",
            "-4" : "Already paid",
            "-5" : "User does not exist",
            "-6" : "Transaction does not exist",
            "-7" : "Failed to update user",
            "-8" : "Error in request from click",
            "-9" : "Transaction cancelled"
        }
        
    def get_error(self, error):
        
        return self.errors.get(str(error))
