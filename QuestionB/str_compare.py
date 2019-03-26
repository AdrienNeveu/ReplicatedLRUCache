def simple_compare (a, b):
    if a == b:
        return 0
    elif a < b:
        return -1
    else:
        return 1

def compare(a, b):
    # Tries first to treat as floats
    try:
        a = float(a)
        b = float(b)
        return simple_compare(a, b)
    except ValueError:
        # Tries to treat as ints
        try:
            a = int(a)
            a = int(b)
            return simple_compare(a, b)
        except ValueError:
            # Treats as strings
            return simple_compare(a, b)

# Formats 
def cmp_to_english(cmp):
    if cmp == 0:
        return "equal to"
    return "less than" if cmp == -1 else "greater than"
