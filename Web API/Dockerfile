FROM python:3

WORKDIR /app

RUN pip install flask
RUN pip install requests


COPY run_server.py /app/

CMD ["python", "main.py"]