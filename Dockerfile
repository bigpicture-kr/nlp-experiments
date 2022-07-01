FROM tensorflow/tensorflow:latest-gpu

MAINTAINER Seongbum Seo <sbumseo@bigpicture.team>

ENV PYTHONUNBUFFERED 0
WORKDIR /gpt

RUN apt-get update && apt-get install -y git
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install mxnet-cu112 gluonnlp
RUN pip install jupyterlab
RUN pip install ipywidgets
RUN apt-get install -y npm && npm install -g n && n lts

#COPY ./jupyter_lab_config.py /root/.jupyter/jupyter_lab_config.py
#ADD jupyter_lab_config.py /config/jupyter_lab_config.py
#CMD ["jupyter", "lab", "--config", "/config/jupyter_lab_config.py"]

EXPOSE 443

