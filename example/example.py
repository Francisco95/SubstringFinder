import sys
sys.path.append("../")
from source.substring import FindSubstring

'''
Example of usage, for a given text find some substring using regular expressions
'''


# first of all, read the file
file = "text.txt"
text = "".join(list(open(file, 'r').read())[:-1])
# text = text[-1]

# then we can look for any substring, for example:
substring = "|.ab*b"
find_substring = FindSubstring(substring)
find_substring.find(text)

# this should give to you the positions in the text of aparitions, in this case:
# [2, 2]: b
# [3, 3]: b
# [6, 6]: b
# [9, 9]: b
# [21, 21]: b


# you can test these oter examples:
substring2 = "*||z.WQ*.... 12zw"
find_substring2 = FindSubstring(substring2)
substring3 = "*||z.Q\n*...... 12zw \n"
find_substring3 = FindSubstring(substring2)

print("-----")
find_substring2.find(text)
print("-----")
find_substring3.find(text)