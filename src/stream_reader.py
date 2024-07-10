import os
import signal
import sys

import cv2
import freenect
import numpy as np
from init_ressources import create_textures, load_objects_texture
from skimage.io import imsave

WIDTH = 480
HEIGHT = 640

# Initialize fossil objects and bg images
fossil1 = {"name": "human_bone", "path": "objects/bone.png", "scale_factor": 0.25}
fossils = load_objects_texture([fossil1] * 10)
BG_IMG, FG_IMG, Z_IMG = create_textures(fossils, sdbx_width=WIDTH, sdbx_height=HEIGHT)
BG_IMG, FG_IMG, Z_IMG = (
    np.transpose(BG_IMG, (1, 0, 2)),
    np.transpose(FG_IMG, (1, 0, 2)),
    np.transpose(Z_IMG),
)

IID_RGB = 0
IID_DPT = 0
MAX_DEPTH = 3000  # Max depth in mm (adapt with the real depth)
running = True


def sighandler(signal, frame):
    global running
    if signal in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
        running = False
    sys.exit(0)


def depth_callback(dev, data, timestamp):
    imsave("test_depth.png", data)
    imsave("FG.png", FG_IMG)
    imsave("BG.png", BG_IMG)
    # normalize data
    depth_img = np.minimum(data, MAX_DEPTH) / MAX_DEPTH
    mask_z = Z_IMG <= depth_img
    new_image = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
    new_image[mask_z] = FG_IMG[mask_z]
    new_image[~mask_z] = BG_IMG[~mask_z]

    cv2.imshow("Depth Stream", new_image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        global running
        running = False


def rgb_callback(dev, data, timestamp):
    # print("rgb_callback")
    # imsave("test.png", data)
    # print(data.shape)
    # print(data)

    # Convertir le format d'image de RGB Ã BGR pour OpenCV
    # rgb_img = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
    # cv2.imshow("RGB Stream", rgb_img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     global running
    #     running = False
    return


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
    cv2.destroyAllWindows()
    print("Done!")


if __name__ == "__main__":
    main()
