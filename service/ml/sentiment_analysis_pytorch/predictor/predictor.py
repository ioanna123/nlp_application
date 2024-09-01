from typing import List


class SentimentAnalysisTorchPredictor:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def predict(self, suggestions: List[str]) -> List:
        """
        filter suggestions based on sentiment
        @param suggestions: list with suggestions to be filtered
        @return: List
        """
        positive_suggestions = []
        for suggestion in suggestions:
            sentiment = self.pipeline(suggestion)[0]
            if sentiment['label'] == 'POSITIVE':
                positive_suggestions.append(suggestion)

        return positive_suggestions
