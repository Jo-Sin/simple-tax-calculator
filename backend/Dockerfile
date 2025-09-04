FROM python:3.10-slim
WORKDIR /usr/src/app
COPY . .
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "server.py"]