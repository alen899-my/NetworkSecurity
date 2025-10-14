import sys
import os
import certifi
from dotenv import load_dotenv
import pymongo
import pandas as pd

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from uvicorn import run as app_run

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print("Mongo URL:", mongo_db_url)

# MongoDB connection
ca = certifi.where()
try:
    client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
    database = client[DATA_INGESTION_DATABASE_NAME]
    collection = database[DATA_INGESTION_COLLECTION_NAME]
    print("MongoDB connected successfully")
except Exception as e:
    print("MongoDB connection error:", e)

# FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="./templates")

# Allow all CORS origins (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        # Run training in threadpool to avoid blocking
        await run_in_threadpool(train_pipeline.run_pipeline)
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Read CSV
        df = pd.read_csv(file.file)

        # Load preprocessor and model
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        # Predict (run in threadpool)
        y_pred = await run_in_threadpool(network_model.predict, df)
        df['predicted_column'] = y_pred

        # Save output (optional)
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        # Render table
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# Simple test route
@app.get("/test")
async def test():
    return {"message": "Server is running"}


if __name__ == "__main__":
    # Use 0.0.0.0 to allow access from other devices
    app_run(app, host="0.0.0.0", port=8000, reload=True)
