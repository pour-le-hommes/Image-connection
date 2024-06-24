from llama_cpp import Llama
import time
import json
from transformers import AutoTokenizer

# from huggingface_hub import hf_hub_download
# hf_hub_download(repo_id="cfahlgren1/natural-functions-GGUF", filename="natural-functions.Q4_1.gguf")


class Hermes():
    _instances = None

    def __new__(cls):
        if cls._instances is None:
            cls._instances = super(Hermes, cls).__new__(cls)
            cls._instances._model = None
            cls._instances._tokenizer = None
        return cls._instances

    def init(self):
        model_kwargs = {
        "n_ctx":4096,    # Context length to use
        "n_threads":10,   # Number of CPU threads to use
        "n_gpu_layers":2,# Number of model layers to offload to GPU. Set to 0 if only using CPU
        "verbose":False,
        "chat_format":"llama-2",
        }

        ## Instantiate model from downloaded file
        self._model = Llama(
            model_path="models/phi-2.Q5_K_M.gguf",
            **model_kwargs)

    def prompt(self, prompt_messages):
        generation_kwargs = {
            "max_tokens":200, # Max number of new tokens to generate
            "stop":["<|endoftext|>", "<</SYS>>", "[SYS]","[INST]"], # Text sequences to stop generation on
            "top_k":1, # This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
            "temperature":0.9,
            "stream":True
        }

        start_time = time.time()

        output = self._model.create_chat_completion(
            messages=prompt_messages,
            **generation_kwargs
        )
        # Optionally print the total time taken for generation

        # Initialize an empty string to collect the generated content
        generated_text = ""

        # Process each chunk as it arrives
        for chunk in output:
            delta = chunk['choices'][0]['delta']
            if 'role' in delta:
                print(delta['role'], end=': ', flush=True)
            elif 'content' in delta:
                print(delta["content"], end='', flush=True)
                generated_text+=delta["content"]

        end_time = time.time()
        print(f"\n\nTime taken: {end_time - start_time:.2f} seconds\n\n")

        return generated_text