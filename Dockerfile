FROM python:2.7-slim

#install dependencies

RUN apt-get update && apt-get install -y --no-install-recommends python-dev gcc wget postgresql-9.4 libpq-dev

#get raw code from AWS and install requirements

RUN wget -P /aws/ https://raw.githubusercontent.com/awslabs/amazon-redshift-utils/master/src/requirements.txt
RUN wget -P /aws/ https://raw.githubusercontent.com/awslabs/amazon-redshift-utils/master/src/AnalyzeVacuumUtility/analyze-vacuum-schema.py
RUN mv /aws/analyze-vacuum-schema.py /aws/analyze_vacuum_schema.py
RUN	pip install -r /aws/requirements.txt

# Make the image thinner 

RUN apt-get purge -y --auto-remove python3-dev gcc wget libpq-dev

ADD ./entrypoint.py /aws/entrypoint.py
RUN	chmod +x /aws/*

# set up environment variables

ENV DB_SCHEMA public
ENV DB_PORT 5439
ENV OUTPUT_FILE /var/log/log.txt
ENV DEBUG True
ENV VACUUM_PARAM FULL
ENV IGNORE_ERRORS False
ENV VACUUM_FLAG True
ENV ANALYZE_FLAG True
ENV SLOT_COUNT 2
ENV MIN_UNSORTED_PCT 5
ENV MAX_UNSORTED_PCT 50
ENV DELETED_PCT 15
ENV STATS_OFF_PCT 10
ENV MAX_TABLE_SIZE_MB 700*1024
ENV SEND_EMAIL False

ENTRYPOINT ["python", "/aws/entrypoint.py"]