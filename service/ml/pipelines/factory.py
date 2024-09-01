from service.ml.fill_in_pytorch.loader import load_bert_tokenizer, load_bert_model
from service.ml.fill_in_pytorch.predictor.predictor import FillInTorchPredictor
from service.ml.fill_in_pytorch.preprocessor.preprocessor import Preprocessor
from service.ml.pipelines.pipeline import MLPipeline
from service.ml.sentiment_analysis_pytorch.loader import load_bert_pipeline
from service.ml.sentiment_analysis_pytorch.predictor.predictor import SentimentAnalysisTorchPredictor


def create_preprocess() -> Preprocessor:
    return Preprocessor()


def create_fill_in_pipeline(model_name="bert-large-uncased") -> FillInTorchPredictor:
    model = load_bert_model(model_name)
    tokenizer = load_bert_tokenizer(model_name)

    return FillInTorchPredictor(model=model, tokenizer=tokenizer)


def create_sent_anal_pipeline(model_name="distilbert-base-uncased-finetuned-sst-2-english",
                              task="sentiment-analysis") -> SentimentAnalysisTorchPredictor:
    pipeline = load_bert_pipeline(model=model_name, task=task)

    return SentimentAnalysisTorchPredictor(pipeline=pipeline)


def create_ml_pipeline() -> MLPipeline:
    return MLPipeline(
        fill_in=create_fill_in_pipeline(),
        sent_anal=create_sent_anal_pipeline(),
        preprocess=create_preprocess()
    )
