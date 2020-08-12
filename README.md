# What This Code Does

The code in this GitHub repository helps you identify words you look up repeatedly in Pleco's reader function. It takes history backup files from Pleco, determines what subset of words were queried at least twice (at times that were at least five days apart), and then saves those words as a list in a text file.

The five-day time threshold (which can be changed on line 8 of `1_process_pleco_backups.py`) is to account for articles that take more than one day to read.

# Requirements

You will need:

* multiple history backup files from Pleco (e.g. `settingsbackup-1509041749.xml`). Pleco [only saves](https://plecoforums.com/threads/export-search-history-to-text-file.5928/#post-47626) the most recent lookup in the reader history, so this code needs more than one history backup file to work.
* the ability to run Python code on your computer. If you are new to Python I recommend downloading the (free and open-source) [Anaconda](https://www.anaconda.com/products/individual) distribution of Python, because the Python scripts (files with `.py` file extension) in this GitHub repository require some libraries that you won't get if you install Python from the [official website](python.org). The Python scripts can be run from the command line; you don't have to install a sophisticated [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment). This code has been tested to work with Python 3.7.4, but any later version of Python should be OK.

# Steps for Use

1. Download this repository into a folder on your computer (green "Code" button > Download zip).
2. Export your reader lookup history from Pleco: hamburger icon > Settings > Backup Settings and/or History > Backup History Only.
3. Save the `.xml` backup file in the `backups` folder.
4. Read lots of Chinese, look up lots of words in the Pleco reader function, and repeat steps 2 to 3 every couple of weeks. As explained above, this code needs multiple Pleco backup files to work.
5. Run the first Python script. (You can do this on the command line by typing `python 1_process_pleco_backups.py` and pressing enter.) After a few seconds you should see a file `pleco_import.xml` appear in the folder where you saved the code. The file `pleco_import.xml` is structured just like the Pleco backup files you've been saving, except that it only contains reader lookup history entries for words you've looked up on two days that were at least three days apart.
6. Clear your reader lookup history: hamburger icon > History > READER > three-dots icon on top right > Clear current list.
7. Import the file `pleco_import.xml` into Pleco: hamburger icon > Settings > Restore from Backup.
8. Create Pleco flashcards for the reader lookup history entries (you may want to create a separate category for these flashcards if you use Pleco's flashcard function to study): hamburger icon > History > READER > three-dots icon > Dump current list to flashcards. This will take a minute, during which your phone screen may be unresponsive.
9. Export the flashcards as a text file: hamburger icon > Import / Export (under FLASHCARDS) > Export Cards > uncheck all boxes except "Remap if forbidden"
10. Save the text file Pleco just created (it will be called something like `flash-2008111841.txt`) into the folder with the Python code.
11. Open up the text file `known_words.txt` and enter the words you currently know. If you happened to accidentally look up any of these words in the Pleco reader function the code will make sure they don't end up in the final output file. One word per line, and it's OK if there is other stuff on the line after the 汉字 as long as it's separated by a tab. A text file export of cards from Anki will work as long as you rename the file `known_words.txt`.
12. Run the second Python script (`python 2_remove_known_words.py`). This will create a final file called `output.txt`.
13. Learn the words in `output.txt` that look useful.
