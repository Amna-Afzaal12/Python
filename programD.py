def match_strings(str1, str2):
    if str1 == str2:
        return True
    else:
        return False

s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

if match_strings(s1, s2):
    print("Strings match!")
else:
    print("Strings do not match!")
