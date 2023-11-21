# WDPS_Assignment

## Implementation
Four modules
(Can be implemented in one but LLM is separate)

### Customer Service
- Entry point
- Receives: input (.txt file)
- Sends: sends to Delphi
- Reads Delphi output
- Starts Delphi again (How?)
- Accumulates responses from Delphi, Answer Extractor, Entity Linker and sends to Fact Checker
- Gets final response from Fact Checker and creates a .txt file with the response

### Delphi
- LLM provided by the course
- Receives: user input from Customer Service
- Output: LLM response
- **Problem**: LLM exits after first query

### Answer Extractor
- Receives: LLM response
- Sends: Extracted answer to Customer Service

### Entity Linker
- Receives: Input and LLM response
- Sends: Entity Links to WIkipedia to Customer Service

### Fact Checker
- Receives: Input, Response, Entity Links, Extracted answer
- Sends: Fact checked response to Customer Service


## Running the services
Run start_all_apps.sh to start all services
Goal: each service has docker-compose.yaml and Dockerfile

But for now...
### Delphi
Start the LLM by running
```shell
docker build --platform=linux/arm64/v8 -t wdps:latest .
docker run -it wdps:latest
```


