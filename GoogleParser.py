from bs4 import BeautifulSoup as soup
import os
import sys
from pathlib import Path
from math import ceil


#GoogleTakeoutSearchParser V 0.4
#Designed to extract all the google searches from a Google Takeout archive and write them to a txt output file for easy reference

#VERSION 0.4:
#   -corrected improper documentation format
#   -cleaned out obsolete code

def main():
    searches = []
    intro()

def intro():
    print("Google Takeout Search Parser V 0.3")
    for file in os.listdir():                                                   
        if file.endswith(".html"):
            #verifying the file is a valid takeout archive
            with open(file, encoding='utf-8-sig') as f:                         
                verifi = f.readline()
                f.close()
                if "<title>My Activity History</title>" in verifi:              
                    print("Search file detected as {}!" .format(file))          
                    pilot = input("Press enter to begin parsing.")
                    #wipe existing output in directory to prepare for new output file
                    try:
                        os.remove("output.txt")                                 
                    except OSError:                                             
                        pass
                    target = file
                    parsefile(target)                                           
        else:
            didntfindit = True

    #error notification if Takeout archive isn't found in the directory
    if didntfindit == True:
        print("Search file not detected. Have you extracted the file to the directory this program is contained in?")
        print("Directions:\nYour search query file is located in your Google Takeout .zip download.",
            "It should be at \'takeout-20XXXYZ...-001.zip > Takeout > My Activity > Search > MyActivity.html\'. ",
            "Simply copy the \'MyActivity.html\' file to the same directory as this program.\n\n")
        pilot = input("Press enter to search again, or type \"quit\" to exit the program.    >>>")
        if pilot == "quit" or pilot == "QUIT" or pilot == "Quit":
            sys.exit()


def parsefile(filename):
    print("parsing file...")
    #the new line character doesn't seem to work when writing to a file on windows, so the carriage return is replaced with an "@"
    if sys.platform == "win32" or sys.platform == "win64":                      
        crn = '\n'
    else: crn = "\n"
    #retrieving the Teakout archive file
    f = open(filename, encoding='utf-8-sig')                                    
    sp = soup(f, "lxml")                                                        
    f.close()                                                                 
    searches = (sp.findAll("div",{"class":"mdl-grid"},
                                  {"class":"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}))                                                #only keep href links, we don't need anything else
    print("document parsed! Writing queries to file...")
    writefile(searches, crn)                                                    

def writefile(parse, retrn):
    #loading bar values
    bk = ''                                                                     
    perc = -5                                                                   
    bad_vars = 0       
    #setting encoding error flag to false
    encodeerrror = False 
    
    for gh, item in enumerate(parse):                                           
        round = ceil(len(parse) / 20)                                           
        #loading bar code
        if gh % round == 0:                                                     
            try:
                bk += '█'
            except SyntaxError:
                bk += '#'                                                      
            perc += 5                                                           
            print("|{}| {}% complete" .format(bk, perc))                        

        entry = str(item)
        if "Visited" in entry:
            continue
        else:
            linkk = entry.split("</a>")[0]
            linkk = linkk.split("\">")[5]
            time = entry.split("<br/>")[2]
            time = time.split("</div>")[0]
            #create the output file if it doesn't exist and prepare to append to it
            with open("output.txt", 'a', encoding="utf-8") as fle:     
                if "://www.google.com/search?q=" in entry:
                    try:
                        fle.write("{}:   {}{}" .format(time, linkk, retrn))
                    except UnicodeEncodeError:                                     
                        print("WARNING: Unicode Encoding Error in value \"{}\"." .format(item.text))
                        if encodeerrror == False:                                   
                            print("This error means a search query includes a character that isn't contained in the UTF-8 encoding library.")
                            print("Your output file is probably fine, though the above query has been omitted from the output file.")
                            encodeerrror = True                                         
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
