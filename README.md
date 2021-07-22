# repeated-strings
This code will search through a text file and list all repeated strings

The program works on both text files and docx files. It will find any repeated strings in the document longer than the specified minimum (default is 50). All whitespace and punctuation are ignored, as is case. It only looks for repetition in the letters a-z.

## Usage

To run the code on a text file:

```shell
$ python3 repeated_strings.py --source <text file> 
```
To run the code on a MS Word file and look for matches of at least length 20:

```shell
$ python3 repeated_strings.py --docx --minlen 20 --source <docx file>
```
