import os
import cv2
import hydra
import imagehash
from PIL import Image


def frame_dump(video_path, output_path, threshold, hash_size):
    """
    Main frame dumping loop that manages image writing and similarity detection.
    """

    # Instantiate frame counter for file naming
    currentframe = 0
    frames_written = 0
    hash_set = set()
    capture = cv2.VideoCapture(video_path)

    while True:
        retval, frame = capture.read()

        if retval:
            name = f"{output_path}/frame{str(currentframe)}.jpg"

            # Calculate hash for current frame
            hash = hash_calc(frame, hash_size)
            # Determine if frame is different enough to write image
            if hash not in hash_set:
                if similarity_validation(hash, hash_set, threshold):
                    cv2.imwrite(name, frame)
                    print("Creating..." + name)
                    frames_written += 1
            # Add frame hash to set and increment frame counter
            hash_set.add(hash)
            currentframe += 1

        else:
            print(f"Total number of images written to disk: {frames_written}")
            break

    capture.release()


def hash_calc(frame, hash_size):
    """
    Calculates hash from np.array/frame object from VideoCapture object
    """
    image = Image.fromarray(frame)
    hash = imagehash.dhash(image, hash_size=hash_size)
    return hash


def similarity_validation(hash, hash_set, threshold):
    """
    This function acts as a switch for the different scenarios 
    which determine if a frame should be written to image file
    """
    # Don't want to perform dist calc on empty set
    # Also dist calc will always pass if threshold = 0, so it saves time
    if len(hash_set) == 0 or threshold == 0:
        return True

    elif min_distance_calc(hash, hash_set) > threshold:
        return True

    else:
        return False


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

