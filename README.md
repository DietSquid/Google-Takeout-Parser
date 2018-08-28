VERSION 0.4:

-corrected improper documentation format

-cleaned out obselete code
   
   
 Google-Takeout-Parser
A python program for extracting google searches from your google takeout files.

When I tried to look at my google search history from the past seven-ish years, I found that I had over 40 thousand entries to look through, and somehow, having 40 thousand individual entities in a single HTML file is not the most stable way to view data. So in order to actually be able to view my search history, I coded a quick parser that will extract the search queries and write them to a txt file that's a lot easier to navigate.

# Requirements
Google Takeout Parser requires only two repositiries that aren't included by default in python, both of which are easily available through pip:
BeautifulSoup 4
pathlib

# Use
GoogleParser.py can be run by simply double-clicking on it, or running it in a shell. In order for it to detect your "MyActivity" file, it needs to be located in the same directory as the program. The program will detect any html files in the directory and check to see if it's the correct file, so don't worry about keeping the filename the same.

GoogleParser.py will extract all search queries from the file, along with their timestamps, and write them in chronological order in output.txt, which will be created in the same directory as the program. The parser will skip any websites in the file that are included as links you clicked on from your google search. Do not exit the program before it is finished writing, as it might corrupt the txt file.

GoogleParser.py seems to run fine on both Windows and Linux.

# Issues
- Queries with characters not contained in standard UTF-8 encoding seem to create issues in the parser when writing it to file. Until the issue can be better addressed, the parser will attempt to convert the text first, but if it can't, it will ignore the query and notify you of an error.
- ~~The file has sufficient documentation, but the comments are not formatted in the proper method, which makes the reader constantly have to scroll from side to side to read it. This will be addressed soon.~~
- ~~The code needs to be cleaned up somewhat, and the commented out debug sections need to be segregated from the rest of the program or removed entirely.~~
