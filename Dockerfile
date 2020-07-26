FROM python:3
EXPOSE 80
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install -r requirements.txt
ARG stage
ENV ENV=${stage}

CMD python manage.py runserver 0.0.0.0:80