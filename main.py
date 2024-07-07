import face_reader
import facial_recognition_ring
import kiwikset_lock

def main():
    # Downloads and stores latest front door ring camera ding
    download_latest = facial_recognition_ring.main()

    # Step #2: Runs facial recognition on the latest clip availible from the front door camera
    fr = face_reader.FaceRecognition()
    fr.encode_faces()
    face_match, name = fr.run_recognition("C:\\Users\\camar\\OneDrive\\Documents\\Joa Projects\\facial_recognition\\last_clip\\Front_Door_last_clip.mp4")
    print(f"Possible face match: {face_match}, Person: {name}")

    # 3rd and final step: Unlock the door only if given a positive face match

    if face_match:
        success = kiwikset_lock.main()
        if success:
            print("Door unlocked successfully.")
        else:
            print("Failed to unlock the door.")
    else:
        print("No recognized face. Door remains locked.")


if __name__ == "__main__":
    main()



