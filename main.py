from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__=='__main__':
    try:
        trainingPipelineConfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingPipelineConfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(dataingestionartifact)

        ## Data validation start
        data_validation_config=DataValidationConfig(trainingPipelineConfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)