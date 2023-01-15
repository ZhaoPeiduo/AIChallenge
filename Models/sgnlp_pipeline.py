import os
import requests
import multiprocessing
import concurrent.futures

from sgnlp.models.sentic_gcn import (
    SenticGCNConfig,
    SenticGCNModel,
    SenticGCNEmbeddingConfig,
    SenticGCNEmbeddingModel,
    SenticGCNTokenizer,
    SenticGCNPreprocessor,
    SenticGCNPostprocessor,
    download_tokenizer_files,
)

CPU_COUNT = multiprocessing.cpu_count()
MODEL_ARCHIVE_DIR = "./Models/ModelArchive/"


def download_from_url(url, filename, save_path=MODEL_ARCHIVE_DIR):
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(save_path, filename), 'wb').write(r.content)


def download_from_urls(urls, filenames, cpu_count=CPU_COUNT):
    try:
        assert len(urls) == len(filenames)
        num_workers = CPU_COUNT if CPU_COUNT < len(urls) else len(urls)
        with concurrent.futures.ProcessPoolExecutor(num_workers) as executor:
            executor.map(download_from_url, urls, filenames)
    except AssertionError:
        print("number of urls and their corresponding filename does not match.")


def download_models_and_configs(file_names):
    download_tokenizer_files(
        "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_tokenizer/",
        os.path.join(MODEL_ARCHIVE_DIR, "senticgcn_tokenizer"))

    urls = ("https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn/pytorch_model.bin",
            "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/pytorch_model.bin",
            "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
            "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn/config.json",
            "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/config.json")

    download_from_urls(urls, file_names)


def initialize_model():
    os.makedirs(MODEL_ARCHIVE_DIR, exist_ok=True)

    file_names = ("senticgcn_model.bin", "embedding_model.bin", "senticnet.pickle",
                  "senticgcn_model_config.json", "embedding_config.json")

    if not all(x in os.listdir(MODEL_ARCHIVE_DIR) for x in file_names):
        download_models_and_configs(file_names)

    tokenizer = SenticGCNTokenizer.from_pretrained(os.path.join(MODEL_ARCHIVE_DIR, "senticgcn_tokenizer"))

    senticgcn_config = SenticGCNConfig.from_pretrained(
        "./Models/ModelArchive/senticgcn_model_config.json"
    )

    senticgcn_model = SenticGCNModel.from_pretrained(
        "./Models/ModelArchive/senticgcn_model.bin",
        config=senticgcn_config
    )

    embed_config = SenticGCNEmbeddingConfig.from_pretrained(
        "./Models/ModelArchive/embedding_config.json"
    )

    embed_model = SenticGCNEmbeddingModel.from_pretrained(
        "./Models/ModelArchive/embedding_model.bin",
        config=embed_config
    )

    preprocessor = SenticGCNPreprocessor(
        tokenizer=tokenizer, embedding_model=embed_model,
        senticnet="./Models/ModelArchive/senticnet.pickle",
        device="cpu")

    postprocessor = SenticGCNPostprocessor()

    return senticgcn_model, preprocessor, postprocessor


def run_model(inputs):
    senticgcn_model, preprocessor, postprocessor = initialize_model()
    processed_inputs, processed_indices = preprocessor(inputs)
    raw_outputs = senticgcn_model(processed_indices)
    post_outputs = postprocessor(processed_inputs=processed_inputs, model_outputs=raw_outputs)
    return post_outputs


# if __name__ == '__main__':
#     inputs_example = [
#         {  # Single word aspect
#             "aspects": ["service"],
#             "sentence": "To sum it up : service varies from good to mediorce , depending on which waiter you get ; generally it is just average ok .",
#         },
#         {  # Single-word, multiple aspects
#             "aspects": ["service", "decor"],
#             "sentence": "Everything is always cooked to perfection , the service is excellent, the decor cool and understated.",
#         },
#         {  # Multi-word aspect
#             "aspects": ["grilled chicken", "chicken"],
#             "sentence": "The grilled chicken is the most horrible among all the dishes",
#         },
#     ]
#
#     post_outputs = run_model(inputs_example)
#
#     print(post_outputs[0])
#     # {'sentence': ['To', 'sum', 'it', 'up', ':', 'service', 'varies', 'from', 'good', 'to', 'mediorce', ',',
#     #               'depending', 'on', 'which', 'waiter', 'you', 'get', ';', 'generally', 'it', 'is', 'just',
#     #               'average', 'ok', '.'],
#     #  'aspects': [[5]],  Indicate the 0-indexed position of the aspect, including punctuation
#     #  'labels': [0]}
#
#     print(post_outputs[1])
#     # {'sentence': ['Everything', 'is', 'always', 'cooked', 'to', 'perfection', ',', 'the', 'service',
#     #                'is', 'excellent,', 'the', 'decor', 'cool', 'and', 'understated.'],
#     #  'aspects': [[8], [12]],
#     #  'labels': [1, 1]}
#
#     print(post_outputs[2])
