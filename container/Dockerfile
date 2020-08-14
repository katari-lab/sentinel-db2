FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH="/usr/src/app"
COPY . .
RUN mkdir logs
RUN chmod -R 777 "/usr/src/app"
CMD [ "python", "./app/startup.py" ]