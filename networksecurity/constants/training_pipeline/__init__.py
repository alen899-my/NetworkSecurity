import os
import sys
import numpy as np
import pandas as pd

"""
defining common constant variable for training pipeline

"""
TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="phisingData.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

"""
data ingestion constants for training pipeline
"""

DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DATABASE_NAME:str="ALENDB"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float=0.2