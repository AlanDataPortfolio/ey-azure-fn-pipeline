import azure.functions as func
import logging
from functions.cleaning import clean_dataset1, clean_dataset2, clean_dataset3
from functions.enriching import enriching_dataset1, enriching_dataset2, enriching_dataset3
from functions.merging import merging_dataset_1_2, merging_20000_rows
from functions.synthesising import synthesising_method_1, synthesising_method_2

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Cleaning
app.register_blueprint(clean_dataset1.bp)
app.register_blueprint(clean_dataset2.bp)
app.register_blueprint(clean_dataset3.bp)

# Enriching
app.register_blueprint(enriching_dataset1.bp)
app.register_blueprint(enriching_dataset2.bp)
app.register_blueprint(enriching_dataset3.bp)

# Merging
app.register_blueprint(merging_dataset_1_2.bp)
app.register_blueprint(merging_20000_rows.bp) # to gold layer

# Synthesising
app.register_blueprint(synthesising_method_1.bp)
app.register_blueprint(synthesising_method_2.bp)
