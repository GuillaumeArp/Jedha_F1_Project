FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y


RUN pip install pandas streamlit sklearn plotly numpy openpyxl
COPY . /home/app

CMD streamlit run --server.port $PORT app.py