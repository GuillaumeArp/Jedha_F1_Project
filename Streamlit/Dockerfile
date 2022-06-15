FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y


RUN pip install pandas streamlit plotly numpy fastf1 matplotlib nbformat
COPY . /home/app

ENTRYPOINT ["streamlit","run"]
CMD ["00-Home.py"]