FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir /my-app
WORKDIR /my-app
RUN pip install customtkinter
RUN pip install collections
RUN pip install matplotlib
RUN pip install PIL
RUN pip install threading
RUN pip install tkinter 
RUN pip install pandas 
CMD ["python", "./app.py"] 
