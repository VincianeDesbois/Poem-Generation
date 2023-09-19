# 1 - set base image
FROM python:3.9
# 2 - set the working directory
WORKDIR /opt/app
# 3 - copy files to the working directory
COPY . .
# 4 - install dependencies
RUN pip install -r requirements.txt
# 5 - command that runs when container starts
CMD ["python", "/opt/app/app.py"]