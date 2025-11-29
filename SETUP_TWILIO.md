# 🚀 Setting Up Real Phone Calls with Twilio

Follow these steps to connect your AI agent to real phone calls:

## Step 1: Install ngrok (for local testing)

1. Download ngrok from https://ngrok.com/download
2. Extract it to a folder
3. Open a new terminal and run:
   ```
   ngrok http 5000
   ```
4. You'll see a URL like: `https://abc123.ngrok.io`
5. **Keep this terminal open!** Copy the HTTPS URL.

## Step 2: Configure Twilio Webhook

1. Go to your Twilio Console: https://console.twilio.com/
2. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**
3. Click on your Twilio phone number: **+16154842641**
4. Scroll to **Voice Configuration**
5. Under "A CALL COMES IN":
   - Set to: **Webhook**
   - URL: `https://YOUR-NGROK-URL/incoming-call` (replace with your ngrok URL)
   - HTTP Method: **POST**
6. Click **Save**

## Step 3: Test with a Real Call

1. Make sure your AI agent is running (`python -m src.main`)
2. Make sure ngrok is running and connected
3. Call your Twilio number: **+16154842641**
4. The AI will answer in your voice!
5. After the call, check the dashboard for the voice summary

## Step 4: Add Your Contacts

1. Edit `add_contacts.py` and replace the example contacts with your real ones
2. Run: `python add_contacts.py`
3. Your contacts will now be recognized when they call!

## Troubleshooting

**If the call doesn't connect:**
- Check that ngrok is running
- Verify the webhook URL in Twilio includes `/incoming-call`
- Check the terminal for error messages
- Make sure the AI agent is running

**If the AI doesn't respond:**
- Check your OpenAI API key in `config/.env`
- Check your ElevenLabs API key in `config/.env`
- Look at the server logs for errors

## Important Notes

- **ngrok free tier** creates a new URL each time you restart it
- You'll need to update the Twilio webhook URL each time you restart ngrok
- For production, deploy to a service like Render, Railway, or Heroku
- The AI will generate a voice summary after each call ends
