# Use a Python base image
FROM karmaresearch/wdps2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Copy Pipfiles into the container
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Create and set the working directory in the container
WORKDIR /app

# Copy the rest of the application files into the container
COPY . /app/

RUN mkdir /app/output && chown -R 1000:1000 /app/output && chmod -R 777 /app/output


# Download the english model for spacy
RUN python -m spacy download en_core_web_sm

# Download the nltk models
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader popular
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader wordnet


CMD ["python", "entry_point.py", "2>/dev/null"]

