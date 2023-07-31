# base image
FROM python:3.10.12-slim-bookworm

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /streamlit-chatPDF-app

# install c++
RUN apt-get update
RUN apt-get -y install build-essential
#RUN apt-get -qq -y install gcc

# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
RUN pip3 install -r requirements.txt

# copying all files over
COPY . .

# cmd to launch app when container is run
CMD streamlit run ./src/app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'
