import sys, os
import numpy 
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from network_security.entity.artifact_entity import (
    DataValidationArtifact, DataTransformationArtifact
)

from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data, load_object, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered the initiate_data_transformation method of Data_Transformation class")
        try:
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)  
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace({"legitimate":0, "phishing":1})
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e