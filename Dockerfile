FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app
RUN pip install -r requirements.txt

EXPOSE 80
