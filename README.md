# Trade Signal Bot (TradingView → Telegram)

Малък Flask проект, който приема webhook-и от TradingView и праща форматирани сигнали в Telegram чат.

## Файлове
- `app.py` - основното Flask приложение
- `requirements.txt` - зависимости
- `.env.example` - примерен .env файл

## Настройка (локално)
1. Клонирай или свали проекта и влез в папката:
   ```bash
   cd trade_signal_bot
   ```
2. Създай виртуална среда и инсталирай зависимостите:
   ```bash
   python -m venv venv
   source venv/bin/activate   # на Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
3. Създай `.env` файл по пример на `.env.example` и сложи твоя бот токен:
   ```text
   TELEGRAM_BOT_TOKEN=123456789:ABCdefG...
   TELEGRAM_CHAT_ID=6748093240
   ```
   *Важно*: не споделяй токена публично.

4. Стартирай локално:
   ```bash
   python app.py
   ```
   По подразбиране app слуша на `http://0.0.0.0:5000`.

## Тест с curl
```bash
curl -X POST http://localhost:5000/tradingview \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSDT","side":"BUY","price":68000,"comment":"Test alert"}'
```

## Настройка в TradingView (Alert → Webhook)
В полето `Webhook URL` сложи публичния адрес до твоя сървър, например:
```
https://yourdomain.com/tradingview
```

В полето `Message` в TradingView използвай JSON шаблон (пример):
```
{
  "symbol": "{{ticker}}",
  "side": "{{strategy.order.action}}",
  "price": "{{close}}",
  "comment": "{{strategy.order.comment}}"
}
```

- Когато alert се задейства, TradingView ще прати този JSON към `/tradingview` и приложението ще препрати съобщението в Telegram.

## Deploy идеи
- За бърз тест използвай `ngrok`:
  ```bash
  ngrok http 5000
  ```
  и постави `https://xxxxx.ngrok.io/tradingview` като Webhook URL в TradingView.
- За production използвай Render, PythonAnywhere, Heroku, или VPS. Увери се, че имаш HTTPS (TradingView изисква HTTPS за webhook URL).

## Забележки
- В момента няма допълнителна защита (API key). Ако искаш да добавим проверка на header, кажи ми и ще го добавя.
- Увери се, че ботът е добавен в чата/групата и има права да изпраща съобщения.

Успех! Ако искаш, мога да ти подготвя и версия с допълнителни полета (entry/stoploss/takeprofit), логване на всички сигнали в база данни, или webhook със заглавие/authorization header.
