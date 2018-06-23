from bs4 import BeautifulSoup as soup
import os
import sys
from pathlib import Path
from math import ceil


#GoogleTakeoutSearchParser V 0.3
#Designed to extract all the google searches from a Google Takeout archive and write them to a txt output file for easy reference

def main():
    searches = []
    intro()

def intro():
    print("Google Takeout Search Parser V 0.3")
    for file in os.listdir():                                                   #check every file in the directory for an HTML extension
        if file.endswith(".html"):
            with open(file, encoding='utf-8-sig') as f:                         #for every html file, check the first line
                verifi = f.readline()
                f.close()
                if "<title>My Activity History</title>" in verifi:              #valid Takeout files will have this line at the beginning,
                    print("Search file detected as {}!" .format(file))          #which indicates to the program that it can parse it
                    pilot = input("Press enter to begin parsing.")
                    try:
                        os.remove("output.txt")                                 #delete previously generated outputs if they exist,
                    except OSError:                                             #this is just to prevent appending a list of files to an already existing list of files, which would be confusing and Annoying
                        pass
                    target = file
                    parsefile(target)                                           #send the file to the parsefile function
        else:
            didntfindit = True

    if didntfindit == True:
        print("Search file not detected. Have you extracted the file to the directory this program is contained in?")
        print("Directions:\nYour search query file is located in your Google Takeout .zip download.",
            "It should be at \'takeout-20XXXYZ...-001.zip > Takeout > My Activity > Search > MyActivity.html\'. ",
            "Simply copy the \'MyActivity.html\' file to the same directory as this program.\n\n")
        pilot = input("Press enter to search again, or type \"quit\" to exit the program.    >>>")#run the intro function again, essentially just searching for the file again
        if pilot == "quit" or pilot == "QUIT" or pilot == "Quit":
            sys.exit()


def parsefile(filename):
    print("parsing file...")
    if sys.platform == "win32" or sys.platform == "win64":                      #the new line character doesn't seem to work when writing to a file on windows, so the carriage return is replaced with an "@"
        crn = '\n'
        TODO clean up unnecessary programming
        # print("WARNING: Windows system detected.",
        # " New line character has been replaced with {} symbol" .format(crn))    #this just makes it easy to go into the file after the fact and replace all instances of it with a line break in any txt editors
        # print("You'll need to go into the output.txt after it's finished parsing",
        # " and use a \'replace all\' tool to replace the symbol with a new line.")
    else: crn = "\n"
    f = open(filename, encoding='utf-8-sig')                                    #open the Takeout file
    sp = soup(f, "lxml")                                                        #parse the file in lxml format and assign it to memory
    f.close()                                                                   #close the file, since we don't need it anymore
    searches = (sp.findAll("div",{"class":"mdl-grid"},
                                  {"class":"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}))                                                #only keep href links, we don't need anything else
    print("document parsed! Writing queries to file...")
    writefile(searches, crn)                                                    #passes the links and the carriage return character to the write function

def writefile(parse, retrn):
    bk = ''                                                                     #initialize the loading bar
    perc = -5                                                                   #set the loading bar's progress to -5 percent, since it will gain 5 percent upon it's first iteration
    bad_vars = 0                                                                #set the error count to zero
    encodeerrror = False                                                        #set the encode error flag to false
    # for item in parse:
    #     print("{} {}" .format(item.get("href"), item.text))
    for gh, item in enumerate(parse):                                           #iterator that runs through every value in the list and also gives it's place in the list
        round = ceil(len(parse) / 20)                                           #round the length of the list and divide it by the number of iterators we want the loading bar to have
        #Loading bar
        if gh % round == 0:                                                     #only run through this when the iterator has gone through a certain amount of items related to the total number of items divided by the length of the loading bar
            try:
                bk += '█'
            except SyntaxError:
                bk += '#'                                                       #add to the loading bar
            perc += 5                                                           #increase the percentage
            print("|{}| {}% complete" .format(bk, perc))                        #print the loading bar

        entry = str(item)
        if "Visited" in entry:
            continue
        else:
            linkk = entry.split("</a>")[0]
            linkk = linkk.split("\">")[5]
            time = entry.split("<br/>")[2]
            time = time.split("</div>")[0]
            with open("output.txt", 'a', encoding="utf-8") as fle:              #create the output file if it doesn't exist and prepare to append to it
                if "://www.google.com/search?q=" in entry:
                    try:
                        fle.write("{}:   {}{}" .format(time, linkk, retrn))
                    except UnicodeEncodeError:                                      #exception to catch Encoding Errors
                        print("WARNING: Unicode Encoding Error in value \"{}\"." .format(item.text))
                        if encodeerrror == False:                                   #I'm pretty sure this issue has been fixed already, but just in case, this catch will keep the program from crashing when it encounters a weird character
                            print("This error means a search query includes a character that isn't contained in the UTF-8 encoding library.")
                            print("Your output file is probably fine, though the above query has been omitted from the output file.")
                            encodeerrror = True                                         #set the encode error flag to true so it doesn't print this explaination every time
                            bad_vars += 1
                else:
                    continue
    print("{} Search results written to search.txt with {} errors." .format(len(parse), bad_vars))
    exx = input("press return to close this program.")                          #All done!
    sys.exit()

################################################################################
###                                MAIN                                      ###
################################################################################

if __name__ == "__main__":
    while True:
        main()
