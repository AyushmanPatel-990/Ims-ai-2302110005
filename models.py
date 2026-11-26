from dataclasses import dataclass
from build123d import *

@dataclass
class CellSpec:
    r_cell: float   # mm
    h_cell: float   # mm

cells = {
    "18650": CellSpec(r_cell=9.0, h_cell=65.0),
    "21700": CellSpec(r_cell=10.5, h_cell=70.0),
    "4680":  CellSpec(r_cell=23.0, h_cell=80.0),
}

def make_battery_tray(
    spec: CellSpec,
    n: int = 3,
    clearance: float = 0.25,
    wall: float = 3.0,
    floor: float = 2.0,
    pocket_depth_ratio: float = 0.25,
) -> Part:
    """Generates a parametric battery tray for n cells of a given CellSpec."""
    
    # 1. Derive pocket & spacing dimensions from the spec
    r_pocket = spec.r_cell + clearance
    d_pocket = 2 * r_pocket
    pocket_depth = spec.h_cell * pocket_depth_ratio
    pitch = d_pocket + wall

    # 2. Derive overall tray dimensions
    tray_length = n * d_pocket + (n + 1) * wall
    tray_width = d_pocket + 2 * wall
    tray_height = floor + pocket_depth

    # 3. Create base plate centered at origin (bottom on Z=0)
    plate = Box(
        tray_length,
        tray_width,
        tray_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # 4. Create a single pocket cylinder positioned at Z=floor
    pocket = Pos(0, 0, floor) * Cylinder(
        radius=r_pocket,
        height=pocket_depth + 1.0,  # +1mm ensures clean boolean cut through top
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # 5. Subtract n pockets evenly spaced along the X-axis
    for i in range(n):
        x_offset = (i - (n - 1) / 2) * pitch
        plate = plate - pocket.moved(Location((x_offset, 0, 0)))

    return plate


# --- Generate variants using the exact same function ---
tray_18650 = make_battery_tray(cells["18650"], n=3)
tray_21700 = make_battery_tray(cells["21700"], n=4)
tray_4680  = make_battery_tray(cells["4680"],  n=2)

# Optional: inspect in OCP CAD Viewer (VS Code / Jupyter)
# show(
#     tray_18650.moved(Location((0, -50, 0))),
#     tray_21700,
#     tray_4680.moved(Location((0, 65, 0))),
# )
