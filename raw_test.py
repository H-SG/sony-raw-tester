from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy.typing as npt
import rawpy


def get_rb_bayer_neighbours(raw_values_dict: dict[tuple[int, int], int], init_x: int, init_y: int) -> list:
    span: int = 2
    neighbour_coords: set = {(x, y) for x in [init_x - span, init_x, init_x + span] for y in [init_y - span, init_y, init_y + span]}
    neighbour_coords.remove((init_x, init_y))

    return [raw_values_dict.get(coord) for coord in neighbour_coords if coord in raw_values_dict]


def get_g_bayer_neighbours(raw_values_dict: dict[tuple[int, int], int], init_x: int, init_y: int) -> list:
    # for g in bayer we get these distant ones as with r and b
    neighbour_values: list[int] = get_rb_bayer_neighbours(raw_values_dict, init_x, init_y)

    # but we also need the immediately adjacent four diagonals
    diagonal_span: int = 1
    neighbour_coords: set = {(x, y) for x in [init_x - diagonal_span, init_x + diagonal_span] for y in [init_y - diagonal_span, init_y + diagonal_span]}

    return neighbour_values + [raw_values_dict.get(coord) for coord in neighbour_coords if coord in raw_values_dict]


def main(img_path: Path):
    x_max: int
    y_max: int
    raw_values_dict: dict[tuple[int, int], int] = {}

    # these tuples store (pixel_value, max_of_neighbours) for each colour channel
    red_tuples: list[tuple[int, int]] = []
    green_tuples: list[tuple[int, int]] = []
    blue_tuples: list[tuple[int, int]] = []
    bayer_dict: dict[int, str] = {}

    print(f"Loading {img_path.absolute()}")
    with rawpy.imread(str(img_path.absolute())) as raw:
        # load the raw image
        raw_values: npt.NDArray = raw.raw_image
        bayer_filter: npt.NDArray = raw.raw_colors
        bayer_type: str = raw.color_desc.decode()
        y_max, x_max = raw_values.shape

        print("Buidling coord dict")
        # make raw value dict for speed, arguable whether or not this is worth it
        for x, y in product(range(x_max), range(y_max)):
            raw_values_dict[(x, y)] = int(raw_values[y, x])

        # map the bayer array colours to the index value 
        for i, c in enumerate(bayer_type):
            bayer_dict[i] = c

        print("Finding max neighbours, this might take some time...")
        for x, y in product(range(x_max), range(y_max)):
            colour: str = bayer_dict[bayer_filter[y, x]]
            value: int = raw_values_dict[(x, y)]

            match colour:
                case "R":
                    red_tuples.append((value, max(get_rb_bayer_neighbours(raw_values_dict, x, y))))
                case "G":
                    green_tuples.append((value, max(get_g_bayer_neighbours(raw_values_dict, x, y))))
                case "B":
                    blue_tuples.append((value, max(get_rb_bayer_neighbours(raw_values_dict, x, y))))
        
        print("Plot value against max neighbours")
        plt.figure()
        plt.title(img_path.name)
        plt.scatter([x[1] for x in red_tuples], [x[0] for x in red_tuples], color="red", alpha=0.5)
        plt.xlabel("Max Neighbours")
        plt.ylabel("Pixel Value")
        plt.show(block=False)

        plt.figure()
        plt.title(img_path.name)
        plt.scatter([x[1] for x in green_tuples], [x[0] for x in green_tuples], color="green", alpha=0.5)
        plt.xlabel("Max Neighbours")
        plt.ylabel("Pixel Value")
        plt.show(block=False)

        plt.figure()
        plt.title(img_path.name)
        plt.scatter([x[1] for x in blue_tuples], [x[0] for x in blue_tuples], color="blue", alpha=0.5)
        plt.xlabel("Max Neighbours")
        plt.ylabel("Pixel Value")
        plt.show()

if __name__ == "__main__":
    img_path: Path = Path("A6700_ISO1600_300s.ARW")
    main(img_path)