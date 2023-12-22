# Use a Python base image
FROM karmaresearch/wdps2

# Set environment variables
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Copy Pipfiles into the container

# Create and set the working directory in the container
WORKDIR /app

# Copy the rest of the application files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip

# pip install from requirements.txt
RUN pip install -r requirements.txt

# Download the english model for spacy
RUN python -m spacy download en_core_web_sm

# Download the nltk models
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader popular
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader wordnet




CMD ["python", "-u", "example_using_llm.py"]