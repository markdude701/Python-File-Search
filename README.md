# Python-File-Search
#### Python Application for searching and displaying text/n-grams within text files (using the Whoosh resource). Used for searching for text within directories of files.

##### Description
- A Python 3.6 script allowing the user to select a search directory, and then search for a specific term within the text files of that directory.
###### Features 
- Quick Search: Return number of instances of your search within a document (Returns all documents with searched term and instances)
- Return matching/highlighted text
- Return Line Numbers
- User added file extensions (most text file formats are already used)
- Low Resource-Usage: Whoosh and OS, Traceback

###### TL;DR:
- This python script that allows users to search for text in files within a directory
- Python Search and Indexing using the Whoosh resource

##### Basic Console GUI:
```
    1. Use Current Directory ( . )
    2. Use Another directory (X:/~)
    Please selection an option (1/2):1
    Selected Current Directory
    8  Files Indexed



    Documents Written to Schema!
     -###############-   -###############-   - Search Menu -   -###############-   -###############- 
    Please Select an Option:
    1. Quick Search - Search for text/n-grams, Return Directory & Number of Searched Instances
    2. Specific File Search - Search for text, Return Directory & Line Number & Text
    3. Add Searchable File Type
    4. Exit
     -###############-   -###############-  github.com/markdude701  -###############-   -###############- 
    >>> 4
     -###############-   -###############-   -###############-   -###############- 
    Goodbye!

```
##### ToDo:
- Complete option 4 (User filtering)
- 

- Replace console GUI with actual window GUI

##### Resources:
- Whoosh (https://whoosh.readthedocs.io/en/latest/index.html)