from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, traceback

schema = Schema(title=TEXT(stored=True,sortable=True), path=ID(stored=True), content=TEXT(stored=True))
ix = create_in("indexdir", schema)

path = '.'
directories = ''
files = []
results = []
hit = []
formatting = " -###############- "

docNum = 0

file_types = ['.txt','.lua','.md','.sql','.html','.css','.xml','.rtf']

def close():
    try:
        sys.exit() # Or something that calls sys.exit()
    except SystemExit as e:
        sys.exit(e)
    except:
        # Cleanup and reraise. This will print a backtrace.
        # (Insert your cleanup code here.)
        raise

# r=root, d=directories, f = files
def collectDocuments():
    try:
        totalDocs = 0
        for r, d, f in os.walk(path):
            for file in f:
                for i in range(len(file_types)):
                    if file_types[i] in file:
                        #files.append(file)
                        files.append(os.path.join(r, file))
                        totalDocs += 1
    finally:
        print(totalDocs," Files Indexed")
        return;

def writerFiles():
    try:
        writer = ix.writer()
        try:
            global docNum
            docNum = 0
            for f in files:
                directories = f[2:]
                file = open(directories,"r")
                fileContents = file.read()
                if fileContents == "":
                    print(" ")
                else:
                    if path == '.':
                        writer.add_document(title=(str(docNum)), path=(f[1:]), content=fileContents)
                    else:
                        writer.add_document(title=(str(docNum)), path=(f[0:]), content=fileContents)
                
                
                file.close()
                docNum = docNum + 1
            print("Documents Written to Schema!")
        except UnicodeDecodeError:
            print("Exception in WriterFiles: Error Attempting to Read Open File")
        
        except:
            print("Exception in WriterFiles")
    finally:
        writer.commit()
        #print("\n")
        return;

def searchDocuments(stringVar):
    try:
        global results
        global hit
        instances = 0
        searcher = ix.searcher()
        queryContent = QueryParser("content", ix.schema)
        queryPath = QueryParser("path", ix.schema)
        queryParsed = queryContent.parse(str(stringVar))
        results = ix.searcher().search(queryParsed)
        results[0]
    
    finally:
        
        try:
            found = results.scored_length()
            if results.has_exact_length():
                print("Displaying", found, "of exactly", len(results), "documents")
            else:
                low = results.estimated_min_length()
                high = results.estimated_length()
                print("Displaying", found, " between ", low, "and", high, "documents")
            print("\n")
            print("Titles Found:")
            for hit in results:
                print("(#",hit["title"],") - Path:", hit["path"])
                if path == '.':
                    with open("." + hit["path"]) as myFile:
                        for num, line in enumerate(myFile, 1):
                            if (str(stringVar).upper()) in str(line).upper():
                                instances += 1
                else:
                    with open(hit["path"]) as myFile:
                        for num, line in enumerate(myFile, 1):
                            if ((stringVar).upper()) in str(line).upper():
                                instances += 1

                print ('Number of Instances:', instances,'\n')
                instances = 0
        except:
            print("Exception in Display")
        return;
    #searcher.close()

def numInstances(myFile,instances):
    for num, line in enumerate(myFile, 1):
        if str(stringVar) in line:
            instances += 1
    return;
       
def lineReturn(stringVar, userSearch):
    global results
    global hit
    resultsCount = 0
    for hit in results:
        if hit["title"] == userSearch:
            print("Searched term",stringVar,"in",hit["path"])
            print()
            if path == '.':
                with open("." + hit["path"]) as myFile:
                    for num, line in enumerate(myFile, 1):
                        if (str(stringVar).upper()) in str(line).upper():
                            print("Found on line", num," - ", str(line))
                            #print(hit.highlights("content"))
                            resultsCount += 1
            else:
                with open(hit["path"]) as myFile:
                    for num, line in enumerate(myFile, 1):
                        if ((stringVar).upper()) in str(line).upper():
                            print("Found on line", num," - ", str(line))
                            resultsCount += 1
            print("\n")
            print("Loaded",resultsCount,"instances of searched term!")
    return;

def lineHighlight(stringVar, userSearch):
    global results
    global hit
    resultsCount = 0
    for hit in results:
        if hit["title"] == userSearch:
            print("Searched term",stringVar,"in",hit["path"])
            print()
            if path == '.':
                with open("." + hit["path"]) as myFile:
                    for num, line in enumerate(myFile, 1):
                        if (str(stringVar).upper()) in str(line).upper():
                            print("Found on line", num," - ", hit.highlights("content", top=1000000))
                            #print(hit.highlights("content"))
                            resultsCount += 1
            else:
                with open(hit["path"]) as myFile:
                    for num, line in enumerate(myFile, 1):
                        if ((stringVar).upper()) in str(line).upper():
                            print("Found on line", num," - ", hit.highlights("content", top=1000000))
                            resultsCount += 1
            print("\n")
            print("Loaded",resultsCount,"highlighted instances of searched term!")
    return;

def printF():
    global formatting
    print(formatting,formatting,formatting,formatting)


userMenu = 0
try:    
    
    print("1. Use Current Directory ( . )")
    print("2. Use Another directory (X:/~)")
    userDirectory = input("Please selection an option (1/2):")
    if userDirectory == "1":
        print("Selected Current Directory")
    elif userDirectory == "2":
        newUsrDir = input("Enter new directory:")
        path = newUsrDir
        print("Selected",newUsrDir,"as Current Directory")
        userMenu = 0
    else:
        print("Incorrect Input!")
        
    collectDocuments()
    writerFiles()
    while (userMenu == 4) != True:
        print(formatting,formatting,"Search Menu",formatting,formatting)
        print("Please Select an Option:")
        print("1. Quick Search - Search for text/n-grams, Return Directory & Number of Searched Instances")
        print("2. Specific File Search - Search for text, Return Directory & Line Number & Text")
        print("3. ")
        print("4. Exit")
        print(formatting,formatting,"©Markdude701",formatting,formatting)
        userMenu = input(">>> ")
        printF()
        if userMenu == "1":
            userSearch = input("Enter Search Term:")
            printF()
            searchDocuments(userSearch)
        elif userMenu == "2":
            userSearch = input("Enter Search Term:")
            printF()
            searchDocuments(userSearch)
            userDoc = input("Enter document number (#): ")
            printF()
            lineReturn(userSearch, userDoc)
            printF()
            userHighlight = input("Highlight Searched Term? (Y/N)")
            if userHighlight == "Y":
                lineHighlight(userSearch, userDoc)
        elif userMenu == "4" or userMenu.upper() == "QUIT" or userMenu.upper() == "EXIT":
            print("Goodbye!")
            break
        else:
            print("Incorrect Input, Try 1,2,3,4")
except Exception as e:
    print(e)