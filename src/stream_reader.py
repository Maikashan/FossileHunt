import os
import signal
import sys

import freenect
from skimage.io import imsave

IID_RGB = 0
IID_DPT = 0
running = True


def sighandler(signal, frame):
    global running
    if signal in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
        running = False
    sys.exit(0)


def depth_callback(dev, data, timestamp):
    print("depth_callback")
    imsave("test_depth.png", data)
    print(data.shape)
    print(data)


def rgb_callback(dev, data, timestamp):
    print("rgb_callback")
    imsave("test.png", data)
    print(data.shape)
    print(data)


def main():
    if not os.path.exists("outs"):
        os.makedirs("outs")

    signal.signal(signal.SIGINT, sighandler)
    signal.signal(signal.SIGTERM, sighandler)
    signal.signal(signal.SIGQUIT, sighandler)

    ctx = freenect.init()
    if ctx is None:
        print("Failed to initialize freenect context")
        sys.exit(1)

    num_devices = freenect.num_devices(ctx)
    if num_devices < 1:
        print("No devices found")
        freenect.shutdown(ctx)
        sys.exit(1)

    dev = freenect.open_device(ctx, 0)
    if dev is None:
        print("Failed to open device")
        freenect.shutdown(ctx)
        sys.exit(1)

    freenect.set_depth_callback(dev, depth_callback)
    freenect.set_video_callback(dev, rgb_callback)
    freenect.set_depth_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_MM)
    freenect.set_video_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.VIDEO_RGB)

    freenect.start_depth(dev)
    freenect.start_video(dev)

    global running
    while running:
        freenect.process_events(ctx)

    print("Shutting down")
    freenect.stop_depth(dev)
    freenect.stop_video(dev)
    freenect.close_device(dev)
    freenect.shutdown(ctx)
    print("Done!")


if __name__ == "__main__":
    main()
