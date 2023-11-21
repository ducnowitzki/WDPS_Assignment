# pull from this image karmaresearch/wdps2
FROM karmaresearch/wdps2

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# WORKDIR /

# COPY . .

# # run "source venv/bin/activate"
# RUN echo $(ls -1 /tmp/dir)
# #RUN ["source", "venv/bin/activate"]

# # RUN pipenv install --system --deploy --i

CMD ["python", "-u", "example_using_llm.py"]

