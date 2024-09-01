from transformers import BertTokenizer, BertForMaskedLM
import torch


def load_bert_tokenizer(name:str):
    """
    Load pre-trained tokenizer
    @param name: tokenizer name
    @return: tokenizer
    """
    return BertTokenizer.from_pretrained(name)


def load_bert_model(model: str) -> torch.nn.Module:
    """
    Loads the `~torch.nn.Module` model based on the predefined model.
    @param model: model name
    @return: The `~torch.nn.Module` model on the appropriate device.
    """
    return BertForMaskedLM.from_pretrained(model)


