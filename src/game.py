import signal
import sys

import cv2
import freenect
import numpy as np
from screeninfo import get_monitors

from init_ressources import create_textures, load_objects_texture

_H = None
_HEIGHT = 640
_WIDTH = 480
_MAX_DEPTH = 630
_A = 0.97


def _find_projector_screen():
    monitors = get_monitors()
    print(monitors)
    if len(monitors) > 1:
        for monitor in monitors:
            if monitor.name.__contains__("HDMI"):
                return monitor
    print(
        "Projector screen not found. Make sure the projector is connected (using"
        " built-in display for now)."
    )
    return monitors[0]


_WINDOW_NAME = "Projector"
_PROJECTOR = _find_projector_screen()
_FRAME_RATE = 60


class Game:
    def __init__(self, fossils_dict):
        self.running = False
        self._init_ctx()
        self._init_ressources(fossils_dict)
        # self._init_handlers()
        self._init_callback()

    def _init_ressources(self, fossils_dict):
        self.bg_img, self.fg_img, self.z_img = create_textures(
            load_objects_texture(fossils_dict),
            sdbx_width=_WIDTH,
            sdbx_height=_HEIGHT,
        )
        self.z_img = _A + (1 - _A) * self.z_img

    def _init_ctx(self):
        self.ctx = freenect.init()
        if self.ctx is None:
            print("Failed to initialize freenect context")
            sys.exit(1)
        self.num_devices = freenect.num_devices(self.ctx)
        if self.num_devices < 1:
            print("No devices found")
            freenect.shutdown(self.ctx)
            sys.exit(1)
        self.dev = freenect.open_device(self.ctx, 0)
        if self.dev is None:
            print("Failed to open device")
            freenect.shutdown(self.ctx)
            sys.exit(1)

    def _sighandler(self, signal, frame):
        if signal in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            self.running = False
            self.destroy()
        sys.exit(0)

    def _init_handlers(self):
        signal.signal(signal.SIGINT, self._sighandler)
        signal.signal(signal.SIGTERM, self._sighandler)
        signal.signal(signal.SIGQUIT, self._sighandler)

    def _display(self, image):
        cv2.namedWindow(_WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.moveWindow(_WINDOW_NAME, _PROJECTOR.x, _PROJECTOR.y)
        cv2.setWindowProperty(
            _WINDOW_NAME,
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN,
        )
        resized_image = cv2.resize(
            image,
            (_PROJECTOR.width, _PROJECTOR.height),
            interpolation=cv2.INTER_AREA,
        )
        cv2.imshow(_WINDOW_NAME, resized_image)
        cv2.waitKey(int(1 / _FRAME_RATE * 1000))  # wait match fps

    def _depth_callback(self, dev, data, timestamp):
        if _H != None:
            data = cv2.warpPerspective(data, _H, (data.shape[1], data.shape[0]))
        depth_img = np.minimum(data, _MAX_DEPTH) / _MAX_DEPTH
        mask_z = self.z_img <= depth_img
        new_image = np.zeros((_WIDTH, _HEIGHT, 3), dtype=np.uint8)
        new_image[mask_z] = self.fg_img[mask_z]
        new_image[~mask_z] = self.bg_img[~mask_z]
        self._display(new_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.running = False

    def _init_callback(self):
        freenect.set_depth_callback(self.dev, self._depth_callback)
        freenect.set_depth_mode(self.dev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_MM)

    def start(self):
        freenect.start_depth(self.dev)
        self.running = True

    def run(self):
        while self.running:
            freenect.process_events(self.ctx)

    def destroy(self):
        freenect.stop_depth(self.dev)
        freenect.stop_video(self.dev)
        freenect.close_device(self.dev)
        freenect.shutdown(self.ctx)
        cv2.destroyAllWindows()
