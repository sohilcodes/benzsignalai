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
IMAGE_URL = 'https://t.me/SohilCodes/3896' # Aapka image link
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
        
        # Caption with details
        msg = (f"🚀 SIGNAL ALERT (QUOTEX)\n\n"
               f"📈 Pair: {pair}\n"
               f"💰 Entry Price: Market Price\n"
               f"🎯 Direction: CALL\n"
               f"⏰ Timeframe: 1 Minute\n"
               f"🕒 Entry Time: {entry_time} IST\n"
               f"🏁 Expiry: {expiry_time} IST\n\n"
               f"⚠️ Note: Trade for 1 minute only!")
        
        # Image ke saath message bhej rahe hain
        await bot.send_photo(chat_id=CHANNEL_ID, photo=IMAGE_URL, caption=msg)
        
        # 2 minute ka wait (1m trade + 1m gap)
        await asyncio.sleep(120) 

async def main():
    while True:
        await send_signal()

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(main())
    
