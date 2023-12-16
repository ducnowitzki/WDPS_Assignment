# Use a Python base image, e.g. alpine-python3
FROM karmaresearch/wdps2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Create and set the working directory in the container
WORKDIR /app

RUN mkdir /app/output && chown -R 1000:1000 /app/output && chmod -R 777 /app/output

# Copy Pipfiles into the container
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of the application files into the container
COPY . /app/

# Expose any necessary ports (if your app uses a specific port)
# EXPOSE <port_number>

# python -m spacy download en_core_web_sm

# Define the command to run the application

# IF not debug: add 2>/dev/null
CMD ["python", "generate_dataset.py"]