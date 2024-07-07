import getpass
import json
from pathlib import Path
import requests
from ring_doorbell import Auth, AuthenticationError, Requires2FAError, Ring

user_agent = "YourProjectName-1.0"  # Change this
cache_file = Path(user_agent + ".token.cache")

def token_updated(token):
    cache_file.write_text(json.dumps(token))

def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code

def do_auth():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    auth = Auth(user_agent, None, token_updated)
    try:
        auth.fetch_token(username, password)
    except Requires2FAError:
        auth.fetch_token(username, password, otp_callback())
    return auth

def list_device_names(ring):
    devices = ring.devices()
    device_names = []
    
    # List RingStickUpCams
    for cam in devices['stickup_cams']:
        print(f"StickUpCam name: {cam.name}")
        device_names.append(cam.name)
    
    # List RingDoorBells
    for doorbell in devices['authorized_doorbots']:
        print(f"DoorBell name: {doorbell.name}")
        device_names.append(doorbell.name)
    
    return device_names

def download_last_clip(ring, device_name):
    devices = ring.devices()
    
    # Check RingStickUpCams
    for cam in devices['stickup_cams']:
        if cam.name == device_name:
            print(f"Downloading last clip from StickUpCam: {cam.name}")
            recording = cam.history(limit=5, kind='motion')[0]  # Fetch last motion event
            recording_url = cam.recording_url(recording['id'])
            response = requests.get(recording_url)
            filename = f"{device_name}_last_clip.mp4"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Recording downloaded as {filename}")
            return
    
    # Check RingDoorBells
    for doorbell in devices['authorized_doorbots']:
        if doorbell.name == device_name:
            print(f"Downloading last clip from DoorBell: {doorbell.name}")
            recording = doorbell.history(limit=100, kind='ding')[0]  # Fetch last ding event
            recording_url = doorbell.recording_url(recording['id'])
            response = requests.get(recording_url)
            filename = f"{device_name}_last_clip.mp4"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Recording downloaded as {filename}")
            return
    
    print(f"No device found with the name: {device_name}")

def main():
    if cache_file.is_file():  # auth token is cached
        auth = Auth(user_agent, json.loads(cache_file.read_text()), token_updated)
        ring = Ring(auth)
        try:
            ring.create_session()  # auth token still valid
        except AuthenticationError:  # auth token has expired
            auth = do_auth()
            ring = Ring(auth)
    else:
        auth = do_auth()  # Get new auth token
        ring = Ring(auth)

    ring.update_data()

    # List all device names
    device_names = list_device_names(ring)

    if not device_names:
        print("No devices found.")
        return

    # Get the device name for downloading the last clip
    device_name = input("Enter the device name: ")

    if device_name in device_names:
        download_last_clip(ring, device_name)
    else:
        print(f"No device found with the name: {device_name}")

if __name__ == "__main__":
    main()
