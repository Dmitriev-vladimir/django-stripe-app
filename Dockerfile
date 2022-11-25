FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "test_task.wsgi"]
