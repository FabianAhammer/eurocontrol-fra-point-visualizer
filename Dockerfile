FROM python:3.10.6
COPY . /FRA
WORKDIR /FRA
RUN pip install -r requirements.txt 
EXPOSE 8050
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "main:server"]