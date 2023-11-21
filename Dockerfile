# pull from this image karmaresearch/wdps2
FROM karmaresearch/wdps2

WORKDIR /

COPY . .

# run venv/bin/activate
RUN . venv/bin/activate




