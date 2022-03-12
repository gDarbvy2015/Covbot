FROM python:3.9
COPY . /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ENV COVBOT_CASES_PATH "/usr/src/app/data/new_cases.csv"
ENV COVBOT_VACCINATIONS_PATH "/usr/src/app/data/vaccinations.csv"
ENV COVBOT_LOGS "/usr/src/app/logs"
ENV COVBOT_DB_PATH "/usr/src/app/lib/database"
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
CMD gunicorn --bind 0.0.0.0:5200 wsgi:app
EXPOSE 5200