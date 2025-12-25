
# FastAPI webhook runner for the bot
from fastapi import FastAPI, Request, Response
import uvicorn
import os

# Import your bot handler (adjust import as needed)
try:
	from main import handle_webhook # You should have a function to process webhook requests
except ImportError:
	handle_webhook = None  # Placeholder if not implemented yet

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
	if handle_webhook is None:
		return Response("Webhook handler not implemented", status_code=501)
	data = await request.json()
	# Pass the data to your bot's webhook handler
	result = await handle_webhook(data)
	return result

@app.get("/set-webhook")
async def set_webhook():
    # Here you would set the webhook URL with your bot provider
    # This is a placeholder implementation
    webhook_url = os.environ.get("WEBHOOK_URL", "https://yourdomain.com/webhook")
    # Call your bot's method to set the webhook
    # e.g., await bot.set_webhook(webhook_url)
    return {"status": "webhook set", "url": webhook_url}

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8018))
	uvicorn.run("fastapi_run:app", host="0.0.0.0", port=port, reload=True)
