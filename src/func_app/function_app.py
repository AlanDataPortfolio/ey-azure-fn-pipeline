import azure.functions as func
import logging
from functions import clean_dataset1

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Cleaning
app.register_blueprint(clean_dataset1.bp)
