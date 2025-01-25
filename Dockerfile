FROM python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY app.py .

CMD ["python", "./app.py"] 

LABEL maintainer="Kiarash Dadpour <Kiarash.dadpour@gmail.com>"
LABEL maintainer="Asal Mahmoudi Nejhad <assalmahmodi82@gmail.com>"
LABEL maintainer="Parnian Pourjafari <>"
LABEL version="1.0"
LABEL description="CPU Schedulers Simulator"
