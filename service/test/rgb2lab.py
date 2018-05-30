from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

color1_rgb = sRGBColor(235,22,53)
color2_rgb = sRGBColor(95,11,61)

# Convert from RGB to Lab Color Space
color1_lab = convert_color(color1_rgb, LabColor)
color2_lab = convert_color(color2_rgb, LabColor)

#Finding the difference
diff = delta_e_cie2000(color1_lab, color2_lab)


print(diff)