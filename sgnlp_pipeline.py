import os
import requests

from sgnlp.models.emotion_entailment import (
    RecconEmotionEntailmentConfig,
    RecconEmotionEntailmentModel,
    RecconEmotionEntailmentTokenizer,
    RecconEmotionEntailmentPreprocessor,
    RecconEmotionEntailmentPostprocessor,
)

# Links to be updated
MODEL_URL = "https://storage.googleapis.com/sgnlp/models/reccon_emotion_entailment/config.json"
CONFIG_URL = "https://storage.googleapis.com/sgnlp/models/reccon_emotion_entailment/pytorch_model.bin"


def download_from_urls(urls, filenames):
    for url, filename in zip(urls, filenames):
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)


def initialize_model():
    if not "Models" in os.listdir('../AIChallenge/'):
        os.mkdir("../AIChallenge/Models")
        if not len(os.listdir('../AIChallenge/Models')) == 2:
            download_from_urls([MODEL_URL, CONFIG_URL], ["pytorch_model.bin", "config.json"])


if __name__ == '__main__':
    initialize_model()
    config = RecconEmotionEntailmentConfig.from_pretrained(
        "../AI Challenge/Model/config.json"
    )
    model = RecconEmotionEntailmentModel.from_pretrained(
        "../AI Challenge/Model/pytorch_model.bin",
        config=config,
    )

    tokenizer = RecconEmotionEntailmentTokenizer.from_pretrained("roberta-base")
    preprocessor = RecconEmotionEntailmentPreprocessor(tokenizer)
    postprocess = RecconEmotionEntailmentPostprocessor()

    input_batch = {
        "emotion": ["happiness", "happiness"],
        "target_utterance": ["Thank you very much .", "Thank you very much ."],
        "evidence_utterance": [
            "How can I forget my old friend ?",
            "My best wishes to you and the bride !",
        ],
        "conversation_history": [
            "It's very thoughtful of you to invite me to your wedding . How can I forget my old friend ? My best wishes to you and the bride ! Thank you very much .",
            "It's very thoughtful of you to invite me to your wedding . How can I forget my old friend ? My best wishes to you and the bride ! Thank you very much .",
        ],
    }
    input_dict = preprocessor(input_batch)
    raw_output = model(**input_dict)
    output = postprocess(raw_output)
    print(output)
