from typing import List

import torch


class FillInTorchPredictor:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def _tokenize(self, sentence: str):
        return self.tokenizer.encode(sentence, return_tensors="pt")

    def predict(self, sentence: str) -> List:
        """
        Predicts the words
        @param sentence: str sentence
        @return: List
        """
        input_ids = self._tokenize(sentence)

        with torch.no_grad():
            output = self.model(input_ids)

        # Decode the top 3 predicted tokens for [MASK]
        mask_token_index = torch.where(input_ids == self.tokenizer.mask_token_id)[1]
        predicted_token_ids = output[0][0, mask_token_index].topk(3).indices.tolist()[0]
        predicted_tokens = self.tokenizer.convert_ids_to_tokens(predicted_token_ids)

        return predicted_tokens
