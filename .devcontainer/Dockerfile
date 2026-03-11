FROM jupyter/base-notebook:latest

RUN pip install --no-cache-dir \
    pymongo \
    langchain \
    langchain-anthropic \
    langgraph \
    langgraph-checkpoint-mongodb \
    requests

# Symlink conda Python to standard paths so VS Code can discover it
USER root
RUN ln -s /opt/conda/bin/python /usr/local/bin/python \
    && ln -s /opt/conda/bin/python /usr/local/bin/python3
USER jovyan
