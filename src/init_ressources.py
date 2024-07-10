import cv2
import numpy as np


class Fossil:
    def __init__(self, name: str, texture: np.array, depth: int, x: int, y: int):
        """ Initialize the fossil object

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
        

def load_objects_texture(fossils_dict: list[dict[str, str]], min_depth: int, max_depth: int) \
    -> list[Fossil]:
    """ Load the objects texture from the objects folder
    """
    fossils = []
    for fossil in fossils_dict:
        path, name, x, y = fossil["path"], fossil["name"], fossil["x"], fossil["y"]
        texture = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        depth = np.random.randint(min_depth, max_depth)
        f = Fossil(name=name, x=x, y=y, depth=depth, texture=texture)
        fossils.append(f)
    return fossils


def create_textures(fossils: list[Fossil], width: int, height: int) \
    -> tuple[np.array, np.array, np.array]:
    """
    Create the initial background, the texture background and the depth background
    
    Args
    ----
    fossils: list[Fossil]
        the list of objects in the sand box
    width: int
        the width of the background
    height: int
        the height of the background
    
    Returns
    -------
    tuple[np.array, np.array, np.array]
        the initial background, the texture background and the depth background
    """
    
    init_bg = np.zeros((width, height, 3), dtype=np.uint8)
    init_bg.fill(255)
    depth_bg = np.zeros((width, height), dtype=np.int16)
    depth_bg.fill(-1)
    texture_bg = init_bg.copy()
    for f in fossils:
        twidth, theight = f.texture.shape[0], f.texture.shape[1]
        top_left_x = f.x - twidth // 2
        top_left_y = f.y - theight // 2

        depth_bg[top_left_x:top_left_x + twidth, top_left_y: top_left_y + theight] = f.depth
        texture_bg[top_left_x:top_left_x + twidth, top_left_y: top_left_y + theight, :] = f.texture
    
    return init_bg, texture_bg, depth_bg


if __name__ == '__main__':
    fossil1 = {
        "name": "human_bone",
        "path": "objects/human_bone.jpg",
        "x": 2000,
        "y": 2000
    }
    fossils = load_objects_texture([fossil1], 30, 90) 
    init_bg, texture_bg, depth_bg = create_textures(fossils, 5000, 5000)
    