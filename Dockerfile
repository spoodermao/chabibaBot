FROM python:3.10

RUN apt update && apt upgrade -y
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt 

COPY bot /bot/

WORKDIR /bot

RUN chown -R nobody:nogroup .

USER nobody

ENTRYPOINT ["python","-u","./bot.py"]
