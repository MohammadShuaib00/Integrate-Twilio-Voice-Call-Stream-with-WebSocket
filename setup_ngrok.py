import os
import subprocess
import time
import webbrowser
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_ngrok():
    # Check if ngrok is installed
    try:
        subprocess.run(["ngrok", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ngrok is not installed or not in PATH.")
        print("Please install ngrok from https://ngrok.com/download")
        return

    # Start the Flask app in the background
    flask_process = subprocess.Popen(["python", "app.py"])
    print("Started Flask app on port 5000")

    # Give Flask a moment to start
    time.sleep(2)

    # Start ngrok
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print("Started ngrok")

    # Wait a moment for ngrok to establish tunnels
    time.sleep(3)

    # Get the ngrok public URL
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        public_url = next(
            (t["public_url"] for t in tunnels if t["proto"] == "https"), None
        )

        if public_url:
            webhook_url = f"{public_url}/twilio-webhook/voice"

            print("\n=== Twilio Configuration Instructions ===")
            print(f"1. Your ngrok public URL is: {public_url}")
            print(f"2. Your webhook URL for Twilio is: {webhook_url}")
            print("3. Configure your Twilio phone number:")
            print("   - Log in to the Twilio Console")
            print("   - Go to Phone Numbers > Manage > Active Numbers")
            print(f"   - Select your phone number: {os.getenv('TWILIO_PHONE_NUMBER')}")
            print("   - Under 'Voice & Fax' > 'A CALL COMES IN', select 'Webhook'")
            print(f"   - Enter the webhook URL: {webhook_url}")
            print("   - Set the method to 'HTTP POST'")
            print("   - Save the configuration")
            print("\n4. Test by calling your Twilio number")
            print("\nPress Ctrl+C to stop the servers when done")

            # Open the ngrok web interface
            webbrowser.open("http://localhost:4040")
        else:
            print("Error: Could not find an HTTPS tunnel in ngrok")
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")

    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok_process.terminate()
        flask_process.terminate()
        print("Done!")


if __name__ == "__main__":
    setup_ngrok()
