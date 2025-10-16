import os
import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig

from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.main_utils.utils import load_object, save_object, evaluate_models
from network_security.utils.main_utils.utils import load_numpy_array_data
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("fq_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score) 
            mlflow.sklearn.log_model(best_model, "model")



    def train_model(self, x_train, y_train, x_test, y_test):
        """
        function to train model
        :param x_train: training input features
        :param y_train: training output features
        steps follwed:
        1. define models
        2. define parameters
        3. evaluate models
        4. get best model
        5. get best model score
        6. return the best model
        7. save the model
        8. return the model artifact
        9. logging the artifact
        :return: trained model
        """
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }

        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                # 'splitter': ['best', 'random'],
                # 'max_features': ['sqrt', 'log2'],
            },
            "Random Forest": {
                # 'criterion': ['gini', 'entropy', 'log_loss'],
                # 'max_features': ['sqrt', 'log2', None],
                'n_estimators': [8, 16, 32, 128, 256]
            },
            "Gradient Boosting": {
                # 'loss': ['log_loss', 'exponential'],
                'learning_rate': [.1, .01, .05, .001],
                'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                # 'criterion': ['friedman_mse', 'squared_error'],
                # 'max_features': ['sqrt', 'log2', 'auto'],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            "Logistic Regression": {},#{
                #'penalty': ['l1', 'l2', 'elasticnet', 'none'],
                #'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
            #},
            "AdaBoost": {
                'learning_rate': [.1, .01, .001],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            }
        }

        model_report: dict =evaluate_models(x_train=x_train,y_train=y_train, 
                                             x_test=x_test, y_test=y_test,
                                             models=models, param=params)
        
        ## to get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        ## to get the best model name
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        y_train_pred=best_model.predict(x_train)

        classification_train_metric =get_classification_score(y_true=y_train, y_pred=y_train_pred)

        ## to trach the MLFLOW
        """
        track the experiments with mlflow
        """
        self.track_mlflow(best_model, classification_train_metric)

        y_test_pred=best_model.predict(x_test)
        classification_test_metric =get_classification_score(y_true=y_test, y_pred=y_test_pred)
        self.track_mlflow(best_model, classification_test_metric)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_model)

        ### Model trainer artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                            test_metric_artifact=classification_test_metric)
        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact

        
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            # load the data from data transformation artifact
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # load the training array and testing array
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)
            logging.info(f"loaded train and test array")

            # X_train, y_train, X_test, y_test
            x_train, y_train, x_test, y_test = (
                train_array[:,:-1], 
                train_array[:,-1], 
                test_array[:,:-1], 
                test_array[:,-1]
            )

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)