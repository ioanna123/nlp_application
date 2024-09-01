import logging
from typing import List

from service.ml.fill_in_pytorch.predictor.predictor import FillInTorchPredictor
from service.ml.fill_in_pytorch.preprocessor.preprocessor import Preprocessor
from service.ml.sentiment_analysis_pytorch.predictor.predictor import SentimentAnalysisTorchPredictor

logger = logging.getLogger(__name__)


class MLPipeline:
    def __init__(self,
                 fill_in: FillInTorchPredictor,
                 sent_anal: SentimentAnalysisTorchPredictor,
                 preprocess: Preprocessor):
        self.fill_in = fill_in
        self.sent_anal = sent_anal
        self.prep = preprocess

    def pipeline(self, sentence: str) -> List:
        pre_sent = self.prep.transform(sentence)
        logger.debug(f"Preprocess step from {sentence} to {pre_sent}")

        print("pre_sent", pre_sent)
        suggestions = self.fill_in.predict(pre_sent)
        logger.debug(f"Fill in step from {pre_sent} to {suggestions}")

        return self.sent_anal.predict(suggestions) if suggestions else []
