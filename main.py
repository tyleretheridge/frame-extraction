import os
import cv2
import hydra
import imagehash
from PIL import Image


def frame_dump(video_path, output_path, threshold, hash_size):

    print(f"Video Path: {video_path}")
    capture = cv2.VideoCapture(video_path)

    # Instantiate frame counter
    currentframe = 0
    hash_set = set()

    while True:
        retval, frame = capture.read()

        if retval:
            name = f"{output_path}/frame{str(currentframe)}.jpg"

            # Calculate hash for current frame
            hash = hash_store(frame)
            print(hash)

            # Add first frame to hash_set and write image
            if len(hash_set) == 0:
                hash_set.add(hash)
                cv2.imwrite(name, frame)
                print("Creating..." + name)

            else:

                # Determine if frame is different enough to write image

                threshold = 3

                if hash not in hash_set:
                    min_dist = min_distance_calc(hash, hash_set)
                    hash_set.add(hash)
                    if min_dist > threshold:
                        cv2.imwrite(name, frame)
                        print("Creating..." + name)

            currentframe += 1

        else:
            break

    capture.release()


def hash_store(frame):
    """
    Calculates hash from np.array/frame object from VideoCapture obj
    """
    image = Image.fromarray(frame)
    hash = imagehash.dhash(image, hash_size=8)
    return hash


def min_distance_calc(hash, hash_set):
    """
    Calculates minimum distance between current frame hash and previously calculated hashes
    """
    distances = set()
    for hashes in hash_set:
        distances.add(abs(hash - hashes))

    return min(distances)


# Make data dir to store
def make_dir(output_path):
    """
    Creates images directory for images to be written to
    """
    try:
        if not os.path.exists(output_path):
            print(f"Creating output directory at: {output_path}")
            os.mkdir(output_path)

    except OSError:
        # Make output dir constant and add to msg
        print(f"Error creating directory for images")


@hydra.main(config_path=".", config_name="config")
def main(cfg):

    make_dir(cfg.paths.output_path)
    frame_dump(
        video_path=cfg.paths.video_path,
        output_path=cfg.paths.output_path,
        threshold=cfg.params.threshold,
        hash_size=cfg.params.hash_size,
    )


if __name__ == "__main__":
    main()

