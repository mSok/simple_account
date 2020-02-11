FROM python:3.7-slim

WORKDIR /app

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt

EXPOSE 8080
COPY ["./", "./"]

COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

CMD ["start.sh"]