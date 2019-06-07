from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, traceback
import time, sched
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

def fileTypeDisplay():
    print("Current File Types:")
    for i in range(len(file_types)):
        print(file_types[i])
    printF()

def rebuildIndex():
    collectDocuments()
    writerFiles()
    

    
    
    
    
    #######################################################################################################
    
    
    
    

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
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def startPageOne():
            controller.show_frame("PageOne")
        def startPageTwo():
            controller.show_frame("PageTwo")
            
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

        

            
            
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        global path
        global dirText
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        
        
        #dirLabel = ""
        #dirLabel.set("Directory:" + path)
        #dirLabeler = dirLabel.get()
        dirText = ("Directory:" + path)
        
        #dirText.set("Directory:" + path)
        label = tk.Label(self, text="Menu", font=controller.title_font)
        dirLabels = tk.Label(self,  text = dirText)
        
        
        
        
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
        
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter a Search Term:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        textBox=tk.Entry(self)
        searchBtn = tk.Button(self, text="Search",
                           command=lambda: retrieve_input())
        returnBtn = tk.Button(self, text="Return",
                           command=lambda: controller.show_frame("StartPage"))
        results = tk.Listbox(self)
        textBox.pack()
        searchBtn.pack()
        returnBtn.pack()
        results.pack()
        
        def populateListbox(lstt):
            listbox.insert("end", *lstt)
        
        def retrieve_input():
            inputValue=textBox.get()
            print(inputValue)
            controller.show_frame("PageFour")
        
class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Results:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        
        
if __name__ == "__main__":
    app = PySearch()
    app.mainloop()
    
    
    
    