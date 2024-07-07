import os
import requests
from seam import Seam

# Set the environment variable for the current script execution
os.environ['SEAM_API_KEY'] = 'YOUR_API_KEY'

# Get the API key from the environment variable
api_key = os.getenv('SEAM_API_KEY')

if not api_key:
    raise EnvironmentError("SEAM_API_KEY environment variable not set")

# Device ID and unlock URL
device_id = 'Your_device_ID'
unlock_url = f"https://connect.getseam.com/locks/unlock_door"

def initialize_seam(api_key):
    """
    Initializes the Seam object with the given API key.
    """
    return Seam(api_key=api_key)

def get_locks(seam):
    """
    Fetches and prints details of all locks.
    """
    all_locks = seam.locks.list()

    if all_locks:
        some_lock = all_locks[0]  # Assuming the first lock found
        assert some_lock.properties["online"] is True

        print("Lock details:")
        for count, (key, value) in enumerate(some_lock.properties.items(), start=1):
            print(f"{count}: {key} -> {value}")
        
        return some_lock
    else:
        print("No locks found.")
        return None

def unlock_door(api_key, device_id):
    """
    Sends a POST request to unlock the door with the given device ID.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {"device_id": device_id}

    response = requests.post(unlock_url, headers=headers, json=body)

    if response.status_code == 200:
        print("Door Unlocked Successfully")
    else:
        print(f"Failed to unlock the door. Status code: {response.status_code}")
        print(response.text)  # Print response body for more details

def main():
    # Initialize Seam with API key
    seam = initialize_seam(api_key)

    # Get and print lock details
    some_lock = get_locks(seam)

    # Unlock the door if a lock was found
    if some_lock:
        unlock_door(api_key, device_id)

if __name__ == "__main__":
    main()
