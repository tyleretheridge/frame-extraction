import cv2
import os
import imagehash
from PIL import Image

video_path = "./video/donpa.mp4"

frames1 = "1142"

# Make data dir to store
def make_dir():
    try:
        if not os.path.exists("data"):
            os.mkdir("data")

    except OSError:
        print("Error creating directory for data")


def frame_dump(video_path):
    capture = cv2.VideoCapture(video_path)

    # Instantiate frame counter
    currentframe = 0
    hash_set = set()

    while True:
        retval, frame = capture.read()

        if retval:
            name = "./data/frame" + str(currentframe) + ".jpg"

            # Hashes for dupe check
            hash = hash_store(frame)
            print(f"Calculated hash: {hash}")

            if len(hash_set) == 0:
                hash_set.add(hash)
                cv2.imwrite(name, frame)
                print("Creating..." + name)

            else:
                threshold = 3

                if hash not in hash_set:
                    distances = set()
                    for prev_hash in hash_set:
                        dist = abs(hash - prev_hash)
                        distances.add(dist)

                    hash_set.add(hash)

                    print(f"Distances: {distances}")
                    if min(distances) > threshold:
                        cv2.imwrite(name, frame)
                        print("Creating..." + name)

            currentframe += 1

        else:
            break

    capture.release()


def hash_store(frame):
    image = Image.fromarray(frame)
    hash = imagehash.dhash(image, hash_size=8)
    return hash


def main():
    print(video_path)
    make_dir()
    frame_dump(video_path=video_path)


if __name__ == "__main__":
    main()


# calc distances
# take min distance
# if min distance > threshold, consider a new image
