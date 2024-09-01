from service.ml.pipelines.factory import create_ml_pipeline

input_sentence = "have a [MASK] day"
pipeline = create_ml_pipeline()

results = pipeline.pipeline(input_sentence)

print(results)
