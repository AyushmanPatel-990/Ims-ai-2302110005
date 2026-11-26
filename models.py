
from dataclasses import dataclass
from cadquery import func as cf


@dataclass
class CellSpec:
    r_cell: float
    h_cell: float


def make_cell(spec):
    """Create a simple cylindrical battery model."""
    return cf.cylinder(
        d=2 * spec.r_cell,
        h=spec.h_cell
    )


def tray(
    spec,
    n=3,
    clearance=0.3,
    wall=4.0,
    thickness=6.0,
    depth=3.0,
    mounting_hole_d=5.5,
    mounting_tab=12.0,
):
    """
    Create a 3-cell battery tray with two mounting holes.

    mounting_tab: extra length added at each end.
    """

    pocket_r = spec.r_cell + clearance
    pitch = 2 * pocket_r + wall

    # Original tray dimensions
    base_length = n * pitch + wall
    tray_width = 2 * pocket_r + 2 * wall

    # Extend the tray to create mounting tabs
    plate_length = base_length + 2 * mounting_tab

    plate = cf.box(
        plate_length,
        tray_width,
        thickness
    )

    # Battery pocket
    pocket = cf.cylinder(
        d=2 * pocket_r,
        h=depth + 1
    ).moved(z=thickness - depth)

    for i in range(n):
        x = (i - (n - 1) / 2) * pitch

        plate = plate - pocket.moved(x=x)

    # Two mirrored mounting holes
    hole = cf.cylinder(
        d=mounting_hole_d,
        h=thickness + 1
    ).moved(z=-0.5)

    hole_x = base_length / 2 + mounting_tab / 2

    plate = plate - hole.moved(x=hole_x)
    plate = plate - hole.moved(x=-hole_x)

    return plate


cells = {
    "18650": CellSpec(9.0, 65.0),
    "21700": CellSpec(10.5, 70.0),
    "4680": CellSpec(23.0, 80.0),
}


if __name__ == "__main__":
    for name, spec in cells.items():
        t = tray(spec)

        print(
            name,
            t.isValid(),
            round(t.Volume(), 1)
        )

        t.exportStl(f"tray_{name}.stl")
