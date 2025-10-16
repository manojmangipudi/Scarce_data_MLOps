from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.components.model_trainer import ModelTrainer
from network_security.entity.config_entity import ModelTrainerConfig

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

        ## Data Transformation start
        data_transformation_config=DataTransformationConfig(trainingPipelineConfig)
        logging.info("Data Transformation started")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation completed")

        ## Model Trainer
        model_trainer_config=ModelTrainerConfig(trainingPipelineConfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,
                                   data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info(f"Model Trainer Artifact created")



    except Exception as e:
        raise NetworkSecurityException(e,sys)