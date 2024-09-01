from transformers import pipeline


def load_bert_pipeline(model: str, task: str):
    """
    Load the sentiment analysis pipelin
    :param model: model name
    :param task: task name
    :return:
    """
    return pipeline(task, model=model)
