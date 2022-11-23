FROM python

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]
