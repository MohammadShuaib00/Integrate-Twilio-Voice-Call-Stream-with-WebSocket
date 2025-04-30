# Twilio Voice Call Stream to WebSocket

This application provides a webhook handler for Twilio to stream incoming voice calls to a WebSocket endpoint.

## Features

- Receives incoming calls from a Twilio phone number
- Generates TwiML response with `<Connect>` and `<Stream>` elements
- Streams the audio from the call to a specified WebSocket URL
- Includes security validation for Twilio requests

## Setup

### Prerequisites

- Python 3.x
- pip (Python package manager)
- A Twilio account with a phone number
- ngrok (for local development and testing)

### Installation

1. Clone this repository or download the source code.

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Configure the environment variables in the `.env` file:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   WEBSOCKET_URL=your_websocket_url
   STREAM_TRACK=inbound_track  # or outbound_track, both_tracks
   ```

### Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```

2. Expose your local server using ngrok:
   ```
   ngrok http 5000
   ```

3. Configure your Twilio phone number to use the ngrok URL as the webhook for incoming calls:
   - Log in to the Twilio Console
   - Go to Phone Numbers > Manage > Active Numbers
   - Select your phone number
   - Under "Voice & Fax" > "A CALL COMES IN", select "Webhook"
   - Enter the ngrok URL + `/twilio-webhook/voice` (e.g., `https://xxxx-xx-xx-xx-xx.ngrok.io/twilio-webhook/voice`)
   - Set the method to `HTTP POST`
   - Save the configuration

## Security Considerations

- The application includes Twilio request validation to ensure that only legitimate requests from Twilio are processed.
- Sensitive information is stored in environment variables and loaded using python-dotenv.
- For production deployment, make sure to enable the request validation code in `app.py`.

## Testing

To test the application:
1. Make sure the Flask server is running and exposed via ngrok
2. Call your Twilio phone number
3. Check the logs in your Flask application to confirm the webhook is being received
4. Verify that your WebSocket server is receiving the audio stream from Twilio

## Deployment

For production deployment:
1. Deploy the application to a server with a public IP address
2. Configure your Twilio phone number to use the public URL as the webhook
3. Enable the request validation code in `app.py`
4. Set up proper logging and monitoring

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Integrate-Twilio-Voice-Call-Stream-with-WebSocket
# Integrate-Twilio-Voice-Call-Stream-with-WebSocket
