import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms.llamacpp import LlamaCpp
import pandas as pd

# Download the model and add to the directory
# E.g. take one from her: https://huggingface.co/TheBloke/Llama-2-7B-GGUF#provided-files
MODEL_PATH = os.path.abspath('llama-2-7b.Q4_K_M.gguf')

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# TODO: handling CPU/GPU/Metal
# Comment this out if you want to use CPU
n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

llm = LlamaCpp(
    model_path=MODEL_PATH,
    # Comment the following out as well if you want to use CPU
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

# TODO: handle \t and "    "
llm_response = pd.read_csv('sample_questions.txt', sep='    ', header=None)
llm_response.columns = ['question_id', 'question']
print(llm_response)
outputs = []
for index, row in llm_response.iterrows():
    # handle \t and
    output = llm._call(row['question'])

    # Clean up the output
    # TODO: more profificent way
    output = output.strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('▁', ' ')

    outputs.append(output)

llm_response['output'] = outputs

# Save dataframe to csv
llm_response.to_csv('output/sample_questions_output.csv')
