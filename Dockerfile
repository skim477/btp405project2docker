#pull official base image
FROM python:3.11.4-slim-buster

#set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 
#Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1
#Prevents Python from buffering stdout and stderr

#install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#copy project
COPY . .

# Copy the wait-for-it script
COPY wait-for-it-master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

