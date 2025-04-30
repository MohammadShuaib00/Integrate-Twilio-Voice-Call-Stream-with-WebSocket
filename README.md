# Twilio Voice Call Stream with WebSocket Integration

This project implements a webhook handler that enables Twilio to stream the audio from incoming voice calls received on a specific Twilio phone number directly to a designated WebSocket endpoint.

## Overview

This application sets up a Flask server that:

1. Receives incoming calls via a Twilio webhook
2. Generates TwiML that instructs Twilio to stream the call audio to a specific WebSocket server
3. Passes call metadata (CallSid, caller number) to the WebSocket server
4. Provides utilities for local testing and development with ngrok

## Project Specifications

- **Twilio Phone Number:** +1(934) 253-0570
- **Target WebSocket URL:** wss://devapi.ivoz.ai/llm-campaigns/ws/groq/?bot=ivoz
- **Webhook Endpoint:** /twilio-webhook/voice (HTTP POST)

## Prerequisites

- Python 3.7+
- A Twilio account with the provided credentials
- ngrok (for local development)
- Internet connection to reach the WebSocket server

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Integrate-Twilio-Voice-Call-Stream-with-WebSocket.git
   cd Integrate-Twilio-Voice-Call-Stream-with-WebSocket
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the provided configuration:
   ```
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=+1(934) 253-0570
   WEBSOCKET_URL=wss://devapi.ivoz.ai/llm-campaigns/ws/groq/?bot=ivoz
   STREAM_TRACK=inbound_track  # Optional, defaults to "inbound_track"
   ```

   > **Note:** Replace `your_twilio_account_sid` and `your_twilio_auth_token` with the actual credentials provided in the task description.

## Usage

### Local Development with ngrok

For local development, you can use the provided `setup_ngrok.py` script to:
1. Start the Flask application
2. Create a public URL with ngrok
3. Display configuration instructions for Twilio

```
python setup_ngrok.py
```

The script will:
- Start the Flask server on port 5000
- Start ngrok to create a public URL
- Display the webhook URL to configure in your Twilio account
- Open the ngrok web interface

### Manual Setup

1. Start the Flask server:
   ```
   python app.py
   ```

2. Expose your local server to the internet using ngrok:
   ```
   ngrok http 5000
   ```

3. Configure your Twilio phone number:
   - Log in to the Twilio Console
   - Go to Phone Numbers > Manage > Active Numbers
   - Select your phone number: +1(934) 253-0570
   - Under 'Voice & Fax' > 'A CALL COMES IN', select 'Webhook'
   - Enter the webhook URL: `https://your-ngrok-url.ngrok.io/twilio-webhook/voice`
   - Set the method to 'HTTP POST'
   - Save the configuration

### Testing

You can test the webhook locally without making an actual phone call using the provided test script:

```
python test_webhook.py
```

This will send a simulated Twilio webhook request to your local server and display the TwiML response.

## How It Works

1. When someone calls your Twilio phone number, Twilio sends a webhook request to your server.
2. Your server responds with TwiML that includes:
   - A welcome message
   - A `<Connect>` element with a `<Stream>` element pointing to your WebSocket server
   - Parameters with call metadata (CallSid, caller number)
   - A closing message

3. Twilio establishes a WebSocket connection to your specified WebSocket server and streams the call audio.
4. Your WebSocket server can process the audio in real-time (e.g., for transcription, analysis, etc.).

## WebSocket Server Requirements

Your WebSocket server should:
1. Accept WebSocket connections from Twilio
2. Handle the audio stream in the format specified by Twilio (mulaw audio at 8kHz)
3. Process the call metadata passed as parameters

## Environment Variables

| Variable | Description | Value | Required |
|----------|-------------|-------|----------|
| TWILIO_ACCOUNT_SID | Twilio Account SID | *Use the value from task description* | Yes |
| TWILIO_AUTH_TOKEN | Twilio Auth Token | *Use the value from task description* | Yes |
| TWILIO_PHONE_NUMBER | Twilio Phone Number | +1(934) 253-0570 | Yes |
| WEBSOCKET_URL | WebSocket server URL | wss://devapi.ivoz.ai/llm-campaigns/ws/groq/?bot=ivoz | Yes |
| STREAM_TRACK | Track to stream | inbound_track | No |

## Security Considerations

- **Auth Token:** The Twilio Auth Token is sensitive information. In a production environment, it should be stored securely and not committed to version control.
- **Request Validation:** The application includes Twilio request validation to ensure that only legitimate requests from Twilio are processed.

## Resources

- [Twilio Voice Call Stream Documentation](https://www.twilio.com/docs/voice/twiml/stream)
- [Twilio TwiML Documentation](https://www.twilio.com/docs/voice/twiml)
- [Twilio Request Validation](https://www.twilio.com/docs/usage/security#validating-requests)
- [ngrok Documentation](https://ngrok.com/docs)
