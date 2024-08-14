FROM python:3.10-bullseye

RUN apt-get update
RUN apt-get -y install libhdf5-dev
RUN apt-get -y install texlive-latex-base
RUN apt-get -y install texlive-latex-extra
RUN apt-get -y install latexmk
RUN apt-get install python3-pip -y
RUN pip install -U pip

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

