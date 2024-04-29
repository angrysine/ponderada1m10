FROM python:latest

WORKDIR /app

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN touch sqlite.db

RUN python create_table.py

CMD ["python", "app.py"]