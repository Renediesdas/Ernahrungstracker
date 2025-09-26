FROM python:3-slim

WORKDIR /data

COPY data/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#COPY data/ .

CMD ["python", "app.py"]
