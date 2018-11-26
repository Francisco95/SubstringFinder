# Substring finder

By using properties of regular expressions and automaton theory, we create a simple code to find aparitions of substring in any text.

Code created by Francisco Muñoz with free distribution acording to [MIT License](LICENSE)

## Implementation

Let be AFND a non-deterministic automaton, with an alphanumeric alphabet in adition to white 
space and new line characters. We can construct this AFND from a regular expression by using the 
Thompson method.

Then, since a non-deterministic automaton cannot give a deterministic result, we transform
this into a deterministic automaton, called AFD, this transformation is done by definition using 
the $\epsilon-closure$ and his propagation.


Having the construction of the AFD we can give to the automaton any text (composed only of characters in the previously defined alphabet)
and start the automaton. Every time that we visit a final state of the AFD, we have passed a valid substirng.
In this way we get all the ends positions of all the substring.

To find the initial positions in the text of the substrings, we inverte all the 
transitions of the AFND, transform it to AFD and starting from every one of the 
previously found end positions, 
we scan the text in reverse looking for the start point.

This method will not give all the substring positions, because it doesn't consider
the case when a substring is contained in other substring and both shares the same
end positions, this will give just the smaller substring. 

## Example

There is a simple example code [here](example/example.py) where you can run the
program and see how it works. Explaining a little the example:

* in file.txt store the following tex:
    ```
    "aabb aba bzWQ\n 12zw\n bb"
    ```
   where "\n" correspond to the new line character.
* then define any regular expression in prefix notation, for example:
    ```
    re = "\*||z.WQ*.... 12zw"
    ```
* You can find aparitions of a substirng defined by the regular expression by doing:
    ```
    from source.substring import FindSubstring
    
    # read file
    text = "".join(list(open("file.txt", 'r').read())[:-1])
    
    
    # create substirng instance
    find_substring = FindSubstring(re)
    # find apparitions
    find_substring.find(text) # this print the result
    ```
    
* also in source code there is a file runme.py that you can directly run giving
the file and the regular expression as inputs:

    ```
    python3 runme.py file.txt "\*||z.WQ*.... 12zw"
    ```
    
   where the expression is passes in " " to avoid problems with white space character.
   
   
## Considerations

The whole code was programed in pycharm IDE using a native installation of python 3.6 on
linux system (Ubuntu 18.04), it was also tested on windows using same IDE pycharm.
The packages required in python are just the standard ones.

This code was developed as an assignment for the course "Computer theory" 
imparted in Faculty of Physical and Mathematical Sciences of University of Chile. Has
as only purpose to practice the application of theory of regular languages.