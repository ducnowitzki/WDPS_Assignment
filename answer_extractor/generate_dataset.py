import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms.llamacpp import LlamaCpp
import pandas as pd


MODEL_PATH = os.path.abspath('llama-2-7b.Q3_K_M.gguf')

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

# open questions.csv with pandas
questions = pd.read_csv('questions.csv')

print(questions.head())
outputs = []
for index, row in questions.iterrows():
    output = llm._call(row['Input'])

    # Clean up the output
    # TODO: more profificent way
    output = output.strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('▁', ' ')

    outputs.append(output)

if len(outputs) != questions.shape[0]:
    # save outputs as csv with one column named answer
    df = pd.DataFrame(outputs)
    df.columns = ['Answer']
    df.to_csv('output/answers.csv')
else: 
    questions['Answer'] = outputs
    questions.to_csv('output/questions_and_answers.csv')