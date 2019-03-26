import str_compare

a = input("Input string 1: ")
b = input("Input string 2: ")

compare = str_compare.compare(a,b)
print(a + " " + str_compare.cmp_to_english(compare) + " " + b)
