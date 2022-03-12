FROM python:3.9
COPY . /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python scripts/setup.py
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
EXPOSE 5000