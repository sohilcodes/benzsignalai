import asyncio
import os
import telegram
import pytz
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# Flask setup for Render Web Service
app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


# Settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
IMAGE_URL = 'https://t.me/SohilCodes/3896'
IST = pytz.timezone('Asia/Kolkata')

PAIRS = [
    "AUD/NZD (OTC)", "NZD/CAD (OTC)", "USD/BDT (OTC)", "USD/IDR (OTC)",
    "EUR/NZD (OTC)", "NZD/USD (OTC)", "GBP/NZD (OTC)", "USD/NGN (OTC)",
    "USD/MXN (OTC)", "USD/ARS (OTC)", "USD/PKR (OTC)", "USD/EGP (OTC)",
    "USD/INR (OTC)", "CAD/CHF (OTC)", "NZD/CHF (OTC)", "NZD/JPY (OTC)", "USD/BRL (OTC)"
]


async def send_signal():
    bot = telegram.Bot(token=BOT_TOKEN)

    for pair in PAIRS:
        now = datetime.now(IST)
        entry_time = (now + timedelta(minutes=1)).strftime('%H:%M')
        expiry_time = (now + timedelta(minutes=2)).strftime('%H:%M')

        # HTML format with tg-emoji tags.
        # The visible emoji inside the tag (🤖, 📊, etc.) is the FALLBACK
        # shown to clients that don't support premium emoji.
        # The emoji-id decides which actual premium emoji renders.
        msg = (
            f'<tg-emoji emoji-id="5188481279963715781">🤖</tg-emoji> BENZ SIGNAL Ai ALERT (QUOTEX)\n\n'
            f'<tg-emoji emoji-id="5244837092042750681">📊</tg-emoji> Pair: {pair}\n'
            f'<tg-emoji emoji-id="5224257782013769471">💰</tg-emoji> Entry Price: Market Rate\n'
            f'<tg-emoji emoji-id="5449862290834735715">📈</tg-emoji> Direction: CALL\n'
            f'<tg-emoji emoji-id="5386367538735104399">⏱</tg-emoji> Timeframe: 1 Minute\n'
            f'<tg-emoji emoji-id="5440621591387980068">🕐</tg-emoji> Entry Time: {entry_time} IST\n'
            f'<tg-emoji emoji-id="5195458664789457954">🏁</tg-emoji> Expiry: {expiry_time} IST\n\n'
            f'<tg-emoji emoji-id="6271786398404055377">⚠️</tg-emoji> Note: Trade for 1 minute only!'
        )

        try:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=IMAGE_URL,
                caption=msg,
                parse_mode='HTML'
            )
        except telegram.error.BadRequest as e:
            # Caption too long or bad HTML -> fallback: send text first, then photo separately
            print(f"send_photo failed ({e}), falling back to text + photo")
            await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode='HTML')
            await bot.send_photo(chat_id=CHANNEL_ID, photo=IMAGE_URL)

        # 2 minute ka wait (1 min trade + 1 min gap)
        await asyncio.sleep(120)


async def main():
    while True:
        await send_signal()


if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(main())
