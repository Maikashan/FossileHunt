import cv2


class TemporalSmoothing:
    def __init__(self, alpha=0.1):
        self.alpha = alpha
        self.prev_frame = None

    def apply(self, current_frame):
        if self.prev_frame is None:
            self.prev_frame = current_frame
            return current_frame

        smoothed_frame = (1 - self.alpha) * self.prev_frame + self.alpha * current_frame
        self.prev_frame = smoothed_frame
        return smoothed_frame


def remove_flickering(depth_map, kernel_size=5, alpha=0.1):
    # Apply Gaussian filter
    smoothed_map = cv2.GaussianBlur(depth_map, (kernel_size, kernel_size), 0)

    # Apply temporal smoothing if needed
    # (Assuming you have a TemporalSmoothing class as shown above)
    temporal_smoothing = TemporalSmoothing(alpha=alpha)
    smoothed_map = temporal_smoothing.apply(smoothed_map)

    return smoothed_map
