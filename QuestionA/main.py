def line_overlap(x1, x2, x3, x4):
    return min(x1, x4) < max(x1, x4) and max(x2, x3) > min(x2, x3)

coords1 = input("Enter Line 1 (example: 5,6): ").split(",")
coords2 = input("Enter Line 2 (example: 6,7): ").split(",")

overlap = line_overlap(int(coords1[0]), int(coords1[1]), int(coords2[0]), int(coords2[1]))
if overlap:
    print("The two lines overlap.")
else:
    print("The two lines do not overlap.")
