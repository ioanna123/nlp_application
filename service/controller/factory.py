from service.controller.controller import BaseController
from service.db.factories import create_db_engine
from service.ml.pipelines.factory import create_ml_pipeline


def create_base_controller() -> BaseController:

    db_engine = create_db_engine()
    ml_pipeline = create_ml_pipeline()
    return BaseController(
        db_engine=db_engine,
        ml_pipeline=ml_pipeline
    )
