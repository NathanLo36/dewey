# dewey
## Simple File Sorting
Takes files and sorts them into folders by file name.

### Config File Configuration

Filters and the directory to be sorted are stored in plain text in a 'config file', which is any `.txt` file formatted like this:

    absolute\directory\to\be\sorted

    Subtitle 1
    keyword|||folder
    keyword2|||folder2

    Subtitle 2
    keyword3,*keyword4|||folder3
    keyword3,keyword4|||folder4

The directory to be sorted must be in the first line of the config file.

Filters are in the format:

    keyword|||folder

or

    keyword,keyword2|||folder

If the keyword is in the file name, it will be designated to be put into the corresponding folder. Multiple keywords can exist for the same folder. Special characters can be used in keywords, except for these:

    ,/\ 

Placing a `*` in front of a keyword will make it case insensitive.

Using `|||` in a keyword or a folder name is also not advised.

Folders should be stored as absolute directories in the config file.

If multiple keywords for multiple folders exist in the file name, the user shall be informed and the file will not be moved.

Folders will not be moved. The filter file currently in use will not be moved.