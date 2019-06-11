from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, traceback
import time, sched
import array as arr
import tkinter as tk 
from tkinter import * # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
###################################################################################################################
#root = Tk()

path = '.'
directories = ''
files = []
results = []
hit = []
formatting = " -###############- "
prompt = ">>> "
docNum = 0
documentResults = []
usrSearchTerm = ""
s = sched.scheduler(time.time, time.sleep)
#dirText = ''
#dirText = StringVar()

file_types = ['.txt','.lua','.md','.sql','.html','.css','.xml','.rtf']


######################################################################################################################

schema = Schema(title=TEXT(stored=True,sortable=True), path=ID(stored=True), content=TEXT(stored=True))
if not os.path.exists("indexdir"):
    os.makedirs("indexdir")
ix = create_in("indexdir", schema)


def close():
    try:
        exit(0)
        quit(0)
        #sys.exit()
    except SystemExit as e:
        sys.exit(e)
    except:
        #Cleanup and reraise.
        raise

def printF():
    global formatting
    print(formatting,formatting,formatting,formatting)
        
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
        indexResults = (str(totalDocs) + " Files Indexed")
        documentResults.append(indexResults)
        #print(totalDocs," Files Indexed")
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
    global results
    global hit
    global documentResults
    try:
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
                #print("Displaying", found, "of exactly", len(results), "documents")
                displayTagStr = ("Displaying", found, "of exactly", len(results), "documents\n")
                #displayTag = [displayTagStr]
                #print(displayTag
                #print(displayTagStr)
                documentResults.append(str(displayTagStr))
            else:
                low = results.estimated_min_length()
                high = results.estimated_length()
                #print("Displaying", found, " between ", low, "and", high, "documents")
                displayTagStr = ("Displaying", found, "between", low, "and", high, "documents")
                #print(displayTagStr)
                documentResults.append(displayTagStr)
            documentResults.append("\n")
            #print("Titles Found:")
            documentResults.append("Titles Found:")
            appstr = ""
            appStr2 = ""
            for hit in ((results)):
                appStr = str("(#" + hit["title"] + ") - Path:" + hit["path"])
                documentResults.append(appStr)
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
                appStr2 = str("Number of Instances: " + str(instances))
                documentResults.append(appStr2)
                instances = 0
        #except Exception as e:
            #print("Exception in Display:",e)
        except SyntaxError as e:
            print("SearchDocuments syn Error:",e)
        except Exception as e:
            print("Error in searchDocuments:",e)
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
            #print("Searched term",stringVar,"in",hit["path"])
            searchStr = str(("Searched term",stringVar,"in",hit["path"]))
            documentResults.append(searchStr)
            print()
            if path == '.':
                with open("." + hit["path"]) as myFile:
                    for num, line in enumerate(myFile, 1):
                        if (str(stringVar).upper()) in str(line).upper():
                            searchStr = str("Found on line", num," - ", str(line))
                            documentResults.append(searchStr)
                            #print("Found on line", num," - ", str(line))
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

def fileTypeDisplay():
    print("Current File Types:")
    for i in range(len(file_types)):
        print(file_types[i])
    printF()
    return;

def rebuildIndex():
    collectDocuments()
    writerFiles()
    return;
    

    
    
    
    
    #######################################################################################################
    
def retrieve_input(textBox):
    inputValue=textBox.get()
    return(inputValue)
    #controller.show_frame("PageFour")   

def populateListbox(lstt):
    listbox.insert("end", *lstt)
    return;   

def printResults(lst, resultsBox):
    #resultsBox.insert("end","1")
    #resultsBox.insert("end",lst)
    for i in range(len(lst)):
        resultsBox.insert("end",lst[i])
    return;
    

class PySearch(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Py-Search by Markdude701")

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageLine):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        return;
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        return;



        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def startPageOne():
            controller.show_frame("PageOne")
            rebuildIndex()
            return;
        def startPageTwo():
            controller.show_frame("PageTwo")
            return;
            
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Use Current Directory?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Yes",
                            command=lambda: startPageOne())
        button2 = tk.Button(self, text="No",
                            command=lambda: startPageTwo())
        button1.pack()
        button2.pack()
        
class PageTwo(tk.Frame):
    global path
    global dirText
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter Directory:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        textBox=tk.Entry(self, textvariable=dirText)
        button = tk.Button(self, text="Submit",
                           command=lambda: retrieve_input())
        button1 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        textBox.pack()
        button.pack()
        button1.pack()

        def retrieve_input():
            inputValue=textBox.get()
            path = inputValue
            if path != "":
                controller.show_frame("PageOne")
            else:
                controller.show_frame("StartPage")
            print(inputValue)
            print(path)
        return;

        

            
            
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        global path
        global dirText
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        
        ###################################### WIP #################################
        #dirLabel = ""
        #dirLabel.set("Directory:" + path)
        #dirLabeler = dirLabel.get()
        dirText = ("Directory:" + path)
        
        #dirText.set("Directory:" + path)
        label = tk.Label(self, text="Menu", font=controller.title_font)
        dirLabels = tk.Label(self,  text = dirText)
        
        #############################################################################
        
        
        label.pack(side="top", fill="x", pady=10)
        dirLabels.pack(side="top", fill="x", pady=10)
        
        button = tk.Button(self, text="Quick Search",
                           command=lambda: controller.show_frame("PageThree"))
        button2 = tk.Button(self, text="Line Search",
                           command=lambda: controller.show_frame("StartPage"))
        button3 = tk.Button(self, text="Add File Extension",
                           command=lambda: controller.show_frame("StartPage"))
        button4 = tk.Button(self, text="Change Directory",
                           command=lambda: controller.show_frame("StartPage"))
        button5 = tk.Button(self, text="Quit",
                           command=lambda: self.destory)
        button.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        #update_dir(self,dirText)
        dirText = "Directory" + path
        dirLabels.update()


        
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        global documentResults
        global usrSearchTerm
        
        def startSearch(textBox,resultsBox):
            #controller.show_frame("PageOne")
            searchDocuments(retrieve_input(textBox))
            usrSearchTerm = retrieve_input(textBox)
            printResults(documentResults,resultsBox)
            #print(documentResults)
            return;

        def returnButton(resultsBox):
            controller.show_frame("PageOne")
            resultsBox.delete(0,"end")
            return;
        
        def clearBtnDef(resultsBox):
            resultsBox.delete(0,"end")
            for i in range(len(documentResults)):
                resultsBox.delete(i,'end')
            return;
        def lineSearchDef():
            controller.show_frame("PageLine")
            return;
        
            
            
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter a Search Term:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textBox=tk.Entry(self)
        searchBtn = tk.Button(self, text="Search",
                           command= lambda:startSearch(textBox,resultsBox))
        clearBtn = tk.Button(self, text="Clear",
                           command=lambda:clearBtnDef(resultsBox))
        lineBtn = tk.Button(self, text="Line Search",
                           command=lambda:lineSearchDef())
        returnBtn = tk.Button(self, text="Return",
                           command=lambda:returnButton(resultsBox))
        resultsBox = tk.Listbox(self,width=50,yscrollcommand = scrollbar.set)
        
        
        textBox.pack()
        searchBtn.pack()
        lineBtn.pack()
        clearBtn.pack()
        returnBtn.pack()
        resultsBox.pack()

        
        
        
class PageLine(tk.Frame):
    def __init__(self, parent, controller):
        global usrSearchTerm
        def returnButton(resultsBox):
            controller.show_frame("PageThree")
            resultsBox.delete(0,"end")
            return;
        def startSearch(resultsBox):
            #controller.show_frame("PageOne")
            searchDocuments(usrSearchTerm)
            printResults(documentResults,resultsBox)
            #print(documentResults)
            return;
        def startLineSearch(textBox,resultsBox):
            
            printResults(documentResults,resultsBox)
            return;
        
        
        
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Enter a Document Number:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textBox=tk.Entry(self)
        searchBtn = tk.Button(self, text="Select",
                           command= lambda:startLineSearch(textBox,resultsBox))
        #clearBtn = tk.Button(self, text="Clear",
                           #command=lambda:clearBtnDef(resultsBox))
        returnBtn = tk.Button(self, text="Return",
                           command=lambda:returnButton(resultsBox))
        resultsBox = tk.Listbox(self,width=50,yscrollcommand = scrollbar.set)
        
        
        textBox.pack()
        searchBtn.pack()
        #clearBtn.pack()
        returnBtn.pack()
        resultsBox.pack()
        lambda: startSearch(usrSearchTerm)









        
class PageExample(tk.Frame):
    def __init__(self, parent, controller):
                
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="ExampleLabel:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="BUTTON!",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        
        
if __name__ == "__main__":
    app = PySearch()
    app.mainloop()
    
    
    
    