FROM python:3.9
COPY . /app
EXPOSE 5005
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5005", "run:app"]