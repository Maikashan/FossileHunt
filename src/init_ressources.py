import random

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

    print(img1_bg.shape, img2_fg.shape)
    # Update the original image with our new ROI
    bg[y : y + h, x : x + w] = cv2.add(img1_bg, img2_fg)

    return bg


def load_objects_texture(
    fossils_dict: list[dict[str, str]], min_depth: int, max_depth: int
) -> list[Fossil]:
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
        scale_factor = fossil.get("scale_factor", None)
        size = fossil.get("size")

        # Load (and resize) the texture
        texture = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if scale_factor is not None:
            texture = cv2.resize(
                texture,
                (
                    int(texture.shape[1] * scale_factor),
                    int(texture.shape[0] * scale_factor),
                ),
            )
        if size is not None:
            texture = cv2.resize(texture, (size[0], size[1]))

        depth = np.random.randint(min_depth, max_depth)

        f = Fossil(name=name, x=-1, y=-1, depth=depth, texture=texture)
        fossils.append(f)
    return fossils


def create_textures(
    fossils: list[Fossil], sdbx_width: int, sdbx_height: int
) -> tuple[np.array, np.array, np.array]:
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

    init_bg = np.full((sdbx_width, sdbx_height, 3), 255, dtype=np.uint8)
    depth_bg = np.full((sdbx_width, sdbx_height), -1, dtype=np.int16)
    texture_bg = init_bg.copy()
    for f in fossils:
        theight, twidth = f.texture.shape[:2]
        half_theight = theight // 2
        half_twidth = twidth // 2
        min_y = half_theight
        max_y = sdbx_height - half_theight
        min_x = half_twidth
        max_x = sdbx_width - half_twidth

        randomize_count = 0
        while randomize_count < 10:
            y = random.randint(min_y, max_y)
            x = random.randint(min_x, max_x)

            if np.all(
                texture_bg[
                    y - half_theight : y + half_theight,
                    x - half_twidth : x + half_twidth,
                ]
                == 255
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
                break
            randomize_count += 1

    return init_bg, texture_bg, depth_bg


if __name__ == "__main__":
    fossil1 = {"name": "human_bone", "path": "objects/bone.png", "scale_factor": 0.25}
    fossils = load_objects_texture([fossil1] * 10, min_depth=30, max_depth=90)
    init_bg, texture_bg, depth_bg = create_textures(
        fossils, sdbx_width=1000, sdbx_height=1000
    )
    cv2.imwrite("init_bg.jpg", init_bg)
    cv2.imwrite("texture_bg.jpg", texture_bg)
