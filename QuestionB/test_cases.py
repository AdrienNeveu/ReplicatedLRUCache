import str_compare

print("Test cases:")
cases = [
    ("1","1"),
    ("1","2"),
    ("-1","-2"),
    ("-1.5","-1.6"),
    ("2","1"),
    ("1.1","1.2"),
    ("1.2","1.1"),
    ("1.15","1.12"),
    ("1","1.0000000000"),
    ("1.1.1.1.1", "1.1.1.1.2"),
    ("a","b"),
    ("c","a"),
]

for case in cases:
    case_cmp = str_compare.compare(case[0], case[1])
    print(case[0] + " is " + str_compare.cmp_to_english(case_cmp) + " " + case[1]);

