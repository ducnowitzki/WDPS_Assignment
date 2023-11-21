# WDPS_Assignment

## Implementation
Four modules
(Can be implemented in one but LLM is separate)

### Customer Service
- Entry point
- Deals with user input and returns final result
- Receives: input 
- Sends: sends to Delphi
- Reads Delphi output
- Starts Delphi again (How?)

### Delphi
- LLM provided by the course
- Receives: user input from Customer Service
- Output: LLM response
- **Problem**: LLM exits after first query

### Entity Linker
- Receives: LLM response
- Sends: Entity Links to WIkipedia to Customer Service

### Fact Checker
- Receives: Input, Response, Entity Links
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


