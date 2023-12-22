# WDPS_Assignment
This application has been created as part of an assignment for the Web Data Processing Systems course at VU Amsterdam in 2023.

## How to run
### Prerequisites
- Download a LLM and place in the /delphi directory, you can find one here: https://huggingface.co/TheBloke/Llama-2-7B-GGUF#provided-files
- Adjust the MODEL_PATH variable in entry_point.py#L20 to this LLM
- Provide a questions .txt file
- Adjust QUESTION_FILE_PATH in entry_point.py#L14 to the path of this file
- Adjust SERVER_PORT in entry_point.py#L15 to the separator used in the text file

### Recommended: Run in container of provided virtual environment from docker image karmaresearch/wdps2
- Copy the contents of this repository to the container
- Run `source venv/bin/activate` to activate the virtual environment
- Run `pip install -r group2_requirements.txt` to install the required packages
- Run `python entry_point.py 2>/dev/null` to start the application (the 2>/dev/null is to suppress unnecessary output)

### Alternatively: Run with Docker Desktop
- Start Docker Desktop (It should be Docker Desktop, we had trouble with other ways of using Docker)
- Run the script start_app.sh, e.g. by `sh start_app.sh` (maybe you need to make it executable first)
