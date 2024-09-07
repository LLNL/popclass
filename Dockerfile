FROM python:3.10-bullseye

RUN apt-get update
RUN apt-get -y install libhdf5-dev
RUN apt-get -y install texlive-latex-base
RUN apt-get -y install texlive-latex-extra
RUN apt-get -y install latexmk
RUN apt-get -y install cmake libblas-dev liblapack-dev gfortran
RUN apt-get -y install git
RUN apt-get install python3-pip -y
RUN pip install -U pip

RUN git clone https://github.com/JohannesBuchner/MultiNest.git
WORKDIR MultiNest/build
RUN cmake ..
RUN make
RUN make install
WORKDIR ../..
ENV LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
RUN rm -rf MultiNest

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
