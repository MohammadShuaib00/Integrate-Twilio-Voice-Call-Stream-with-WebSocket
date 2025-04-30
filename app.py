from flask import Flask, Response, request
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")
STREAM_TRACK = os.getenv("STREAM_TRACK", "inbound_track")

# Instantiate validator for request validation
validator = RequestValidator(TWILIO_AUTH_TOKEN)


@app.route("/twilio-webhook/voice", methods=["POST"])
def handle_voice_webhook():
    app.logger.info(
        f"Webhook received. Generating TwiML for WebSocket: {WEBSOCKET_URL}"
    )

    # Log the incoming call details
    call_sid = request.form.get("CallSid", "Unknown")
    from_number = request.form.get("From", "Unknown")
    app.logger.info(f"Incoming call from {from_number} with SID {call_sid}")

    # Create TwiML response
    response = VoiceResponse()

    # Add a welcome message (optional)
    response.say("Thank you for calling. Your call is being connected.")

    # Set up the Stream connection
    connect = Connect()
    stream = Stream(url=WEBSOCKET_URL, track=STREAM_TRACK)

    # Add custom parameters if needed by the WebSocket server
    stream.parameter(name="callSid", value=call_sid)
    stream.parameter(name="fromNumber", value=from_number)

    # Append the stream to connect
    connect.append(stream)

    # Append connect to the response
    response.append(connect)

    # Add instructions after connect (if stream fails/ends)
    response.say("The call has ended. Thank you for calling.")

    return Response(str(response), mimetype="application/xml")


@app.route("/", methods=["GET"])
def index():
    """Simple index route to confirm the server is running."""
    return "Twilio Voice Call Stream Webhook Server is running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Use 0.0.0.0 to be accessible externally via ngrok/deployment
    app.run(host="0.0.0.0", port=port, debug=True)
