# Frame-Extraction
---

## What is this?

Frame-Extraction is a tool that takes an input video and outputs image files that are each unique and different from all other frames. This is particularly useful in the case of 2-D animated videos, where drawn frames are duplicated for the rendered video in general, and frame sequences may be used repeatedly in cycles for various effects.


## Installation & How to Use

Download or 
```git clone https://github.com/tyleretheridge/frame-extraction.git``` the repo to your local machine.  
Open the directory in a terminal and run  `pip install -r requirements.txt`. This will install the dependencies.

Current initial implementation of pathing to the desired input video requires placing the video file into the video folder and renaming the file name in `config.yaml > user_paths > video_path`. Simply rename the `test.mp4` section of the line.  

Then, run `python main.py` in terminal while in the root of the repo directory. 

The script will run, and the images will be generated in the `/images` folder. 

***You will need to delete the test images before using the script. They are there to serve as a guide to how the script operates when `test.mp4` is used as an input.***

## How does it work, and how can I improve my results.  

This tool works by using OpenCV2 to step through the video source frame by frame, performing a perceptual image hash algorithm (dhash) on the frame, then storing that hash to use as a cross reference for future video frames to detect duplicates. Along with duplicate hash detection, there is a rudimentary hamming distance calculation done with each previous frame to calculate how different the current hash is from previous hashes. This is specifically useful in getting rid of sequential images that feature little discrepancy, such as a slow pan within a scene. 

The two params in `config.yaml` called `hash_size` and `threshold` determine how sensitive the tool is to changes in a scene.  

Increasing `hash_size` is useful for more visually complex and detailed scenes; however, it can be costly in performance. A higher hash size will capture more detail as it determines the final downsampled resolution as `hash_size + 1` x `hash_size`. Note that changing the hash will have effects on `threshold`.

Changing `threshold` directly impacts cross-frame similarity referencing, as it is the minimum amount of difference between the current frame and *any* previous frame required to save the frame to disk. This contextual amount of difference a change in threshold provides is fairly abstract, and generally varies based on the type of images contained within the source video. In short, increasing the threshold results in fewer, more different images. Decreasing threshold results in more, increasingly granular images. 

If you don't want this similarity detection and only want all distinct images to be output, set `threshold : 0`. 
