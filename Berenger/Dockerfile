FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y


RUN pip install pandas streamlit plotly numpy fastf1 matplotlib raceplotly streamlit-aggrid streamlit-option-menu
COPY . /home/app

CMD streamlit run --server.port $PORT app.py