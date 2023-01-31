FROM python:3.9
WORKDIR /code
COPY requirements.txt /code/requirements.txt

#ADD requirements.txt / 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

#ADD main.txt_to_delete /
# CMD ["uvicorn","app.main:app", "--host","0.0.0.0","--port","80"]
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
