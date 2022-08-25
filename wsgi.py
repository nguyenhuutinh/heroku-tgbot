
from app.main import app
from app.main import bot

import os


APP_URL = "https://telegram-bot-check-name.herokuapp.com"

if __name__ == "__main__":
    print("start main")
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))