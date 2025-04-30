import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_webhook_locally():
    # URL of your local webhook handler
    webhook_url = "http://localhost:5000/twilio-webhook/voice"

    # Simulate Twilio POST parameters
    twilio_params = {
        "CallSid": "CA123456789abcdef123456789abcdef12",
        "From": "+918004000703",
        "To": os.getenv("TWILIO_PHONE_NUMBER"),
        "Direction": "inbound",
        "+12345678901" "CallStatus": "ringing",
    }

    # Send the request
    print(f"Sending test request to {webhook_url}")
    response = requests.post(webhook_url, data=twilio_params)

    # Print the response
    print(f"Status Code: {response.status_code}")
    print("Response Content:")
    print(response.text)

    # Check if the response contains the expected TwiML elements
    if "Connect" in response.text and "Stream" in response.text:
        print(
            "\nSuccess! The webhook is generating the correct TwiML with <Connect> and <Stream> elements."
        )
    else:
        print(
            "\nWarning: The webhook response does not contain the expected TwiML elements."
        )


if __name__ == "__main__":
    test_webhook_locally()
