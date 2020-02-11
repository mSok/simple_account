FROM python:3.7-slim

WORKDIR /app

COPY ["requirements.txt", "./"]
# COPY ["start.sh", "./"]
RUN pip install -r requirements.txt

EXPOSE 5000
COPY ["./src", "./src"]

COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

CMD ["start.sh"]