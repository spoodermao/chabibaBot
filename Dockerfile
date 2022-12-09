FROM python:3.10

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip && \
    pip install python-telegram-bot --pre &&\
    pip install python-dotenv

COPY bot /bot/

WORKDIR /bot

RUN chown -R nobody:nogroup .

USER nobody

ENTRYPOINT ["python","-u","./bot.py"]
