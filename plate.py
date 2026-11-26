Parametric CAD script testing whether moving a through-hole changes a rectangular plate's volume.(day7) 

import cadquery as cq
import math

# Create plate
plate = cq.Workplane("XY").box(80, 50, 10)

# Create hole cylinder and place it at center
hole = cq.Workplane("XY").cylinder(10, 10)  # height=10, radius=10

# Subtract hole from plate
part = plate.cut(hole)

# Calculate volume
volume = part.val().Volume()

print("Valid:", part.val().isValid())
print("Volume:", round(volume, 1))

# Export STL
cq.exporters.export(part, "plate.stl")
print("STL saved as plate.stl")