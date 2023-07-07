# telegram-bot-emo-support

## Getting Started 

Create a virtual python environment
```console
python -m venv .venv
```
Activate the python environment. 
```console
.\.venv\Scripts\activate
```
Install the requirements into the environment.
```console
pip install -r .\requirements.txt
```
Run the bot.py
```console
python .\src\bot.py
```

Other options: use a single python instance or use Anaconda

## BotFather
Use https://t.me/BotFather to create and manage your Telegram bots.
You get your Telegram API Token from BotFather.

## Environemt Variables
### TELEGRAM_API_TOKEN
API token for Telegram obtained by BotFather.
### EMO_SUPPORT_GROUP_ID
Id of the Telgram group receiving the bot's messages.

## Dokcer

Build
```console
docker build . -t lastgenat/telegram-bot-emo-support:tag
```

Build and compose 
```console
docker compose up --build telegram-bot-emo-support
```
Push to Hub
```console
docker push lastgenat/telegram-bot-emo-support:tag
```
