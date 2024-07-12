import random
from typing import Dict, List, Tuple

import cv2
import numpy as np


class Fossil:
    def __init__(self, name: str, texture: np.array, depth: int, x: int, y: int):
        """Initialize the fossil object

        Args
        ----
        name: str
            name of the object
        texture: np.array
            texture of the object
        depth: int
            depth of the object
        x: int
            x position of the object's center in the background
        y: int
            y position of the object's center in the background
        """
        self.name = name
        self.x = x
        self.y = y
        self.depth = depth
        self.texture = texture


def apply_random_rotation(texture: np.array, angle: int = None) -> np.array:
    """
    Apply a random rotation to the texture

    Args
    ----
    texture: np.array
        the texture to rotate
    angle: int (OPTIONAL)
        the angle of the rotation

    Returns
    -------
    np.array
        the rotated texture
    """
    angle = angle if angle is not None else random.randint(0, 360)
    (h, w) = texture.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
    cos_val = np.abs(M[0, 0])
    sin_val = np.abs(M[0, 1])

    new_w = int((h * sin_val) + (w * cos_val))
    new_h = int((h * cos_val) + (w * sin_val))

    # Adjust the rotation matrix to take into account the translation
    M[0, 2] += (new_w / 2) - (w / 2)
    M[1, 2] += (new_h / 2) - (h / 2)

    rotated_image = cv2.warpAffine(texture, M, (new_w, new_h))
    return rotated_image


def overlay_transparent(bg: np.array, overlay: np.array, x: int, y: int) -> np.array:
    """
    Overlay a transparent image on a background image

    Args
    ----
    bg: np.array
        the background image
    overlay: np.array
        the overlay image
    x: int
        top left x position of the overlay image
    y: int
        top left y position of the overlay image

    Returns
    -------
    np.array
        the background image with the overlay image
    """
    # Extract the alpha mask of the RGBA image, convert to RGB
    b, g, r, a = cv2.split(overlay)
    overlay_color = cv2.merge((b, g, r))

    # Apply some simple filtering to remove edge noise
    mask = cv2.medianBlur(a, 5)

    h, w, _ = overlay_color.shape
    roi = bg[y : y + h, x : x + w]

    # Black-out the area behind the logo in our original ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))

    # Mask out the logo from the logo image.
    img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

    # Update the original image with our new ROI
    bg[y : y + h, x : x + w] = cv2.add(img1_bg, img2_fg)

    return bg


def load_objects_texture(fossils_dict: List[Dict[str, str]]) -> List[Fossil]:
    """Load the objects texture from the objects folder

    Args
    ----
    fossils_dict: list[dict[str, str]]
        lists all the fossils that need to be loaded in a dict in the following format
        {
            "name": str,
            "path": str,
            "scale_factor": float,      (OPTIONAL)
            "size": tuple[int, int]     (OPTIONAL)
            "rotation": int             (OPTIONAL)
        }
    min_depth: int
        min depth of each fossil
    max_depth: int
        max depth of each fossil
    """
    fossils = []
    for fossil in fossils_dict:
        # Load params
        path, name = fossil["path"], fossil["name"]

        # Load (and resize) the texture
        texture = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        scale_factor = fossil.get("scale_factor", None)
        if scale_factor is not None:
            texture = cv2.resize(
                texture,
                (
                    int(texture.shape[1] * scale_factor),
                    int(texture.shape[0] * scale_factor),
                ),
            )
        size = fossil.get("size")
        if size is not None:
            texture = cv2.resize(texture, (size[0], size[1]))

        rotation = fossil.get("rotation")
        texture = apply_random_rotation(texture, angle=rotation)
        depth = np.random.random()

        f = Fossil(name=name, x=-1, y=-1, depth=depth, texture=texture)
        fossils.append(f)
    return fossils


def create_textures(
    fossils: List[Fossil], sdbx_width: int, sdbx_height: int
) -> Tuple[np.array, np.array, np.array, np.array]:
    """
    Create the initial background, the texture background and the depth background

    Args
    ----
    fossils: list[Fossil]
        the list of objects in the sand box
    sdbx_width: int
        the width of the background
    sdbx_height: int
        the height of the background

    Returns
    -------
    tuple[np.array, np.array, np.array]
        the initial background, the texture background and the depth background
    """

    init_bg = np.full((sdbx_height, sdbx_width, 3), 0, dtype=np.uint8)
    depth_bg = np.full((sdbx_height, sdbx_width), -1, dtype=np.float32)
    id_bg = np.full((sdbx_height, sdbx_width), -1, dtype=int)
    texture_bg = init_bg.copy()
    for i, f in enumerate(fossils):
        theight, twidth = f.texture.shape[:2]
        half_theight = theight // 2
        half_twidth = twidth // 2
        min_y = half_theight
        max_y = sdbx_height - half_theight
        min_x = half_twidth
        max_x = sdbx_width - half_twidth

        if (max_x - min_x < theight or max_y - min_y < twidth):
            continue

        randomize_count = 0
        while randomize_count < 10:
            y = random.randint(min_y, max_y)
            x = random.randint(min_x, max_x)

            if np.all(
                texture_bg[
                    y - half_theight : y + half_theight,
                    x - half_twidth : x + half_twidth,
                ]
                == 0
            ):
                f.y = y
                f.x = x

                if f.texture.shape[-1] != 4:
                    texture_bg[
                        y - half_theight : y + half_theight,
                        x - half_twidth : x + half_twidth :,
                    ] = f.texture
                else:
                    texture_bg = overlay_transparent(
                        texture_bg, f.texture, x=x - half_twidth, y=y - half_theight
                    )

                depth_bg[
                    y - half_theight : y + half_theight,
                    x - half_twidth : x + half_twidth,
                ] = f.depth
                id_bg[
                    y - half_theight : y + half_theight,
                    x - half_twidth : x + half_twidth,
                ] = np.where(f.texture[:, :, 3] == 0, -1, i)
                break
            randomize_count += 1

    # Swap width and height of each bg
    init_bg = np.transpose(init_bg, (1, 0, 2))
    texture_bg = np.transpose(texture_bg, (1, 0, 2))
    depth_bg = np.transpose(depth_bg)
    id_bg = np.transpose(id_bg)
    return init_bg, texture_bg, depth_bg, id_bg
