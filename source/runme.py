import sys
sys.path.append("../")
from source.substring import FindSubstring

if __name__ == '__main__':
    text = "".join(list(open(sys.argv[1], 'r').read())[:-1])
    print(text, list(text))
    print(text, sys.argv[2], list(sys.argv[2]))
    find_substring = FindSubstring(sys.argv[2])
    find_substring.find(text)