FROM python:3.8-slim
EXPOSE 8080
WORKDIR /SAM
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run streamlit_qa.py --server.port 8080


