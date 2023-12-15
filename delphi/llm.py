import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms.llamacpp import LlamaCpp
import pandas as pd

class LLM:
    def __init__(self, model_path):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        # TODO: handling CPU/GPU/Metal
        # Comment this out if you want to use CPU
        n_gpu_layers = 1  # Metal set to 1 is enough.
        n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

        self.model = LlamaCpp(
            model_path=model_path,
            # Comment the following out as well if you want to use CPU
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
        )

    def generate_answer(self, input):
        return self.model._call(input)
