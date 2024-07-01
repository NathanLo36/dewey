# dewey
## Simple File Sorting
Takes files and sorts them into folders by file name.

### Config File Configuration

Filters and the directory to be sorted are stored in plain text in a 'config file', which is any `.txt` file formatted like this:

    absolute\directory\to\be\sorted
    keyword|||folder
    keyword2|||folder2
    keyword3,keyword4|||folder3
    keyword3,*keyword4|||folder4

The directory to be sorted should be in the first line of this file.

If the keyword is in the file name, it will be designated to be put into the corresponding folder. Multiple keywords can exist for the same folder. Special characters can be used in keywords, except for these:

    ,/\ 

Placing a `*` in front of a keyword will make it case insensitive.

Using `|||` in a keyword or a folder name is also not advised. An empty line is fine, however, and will be skipped over.

Folders should be stored as absolute directories in the config file.

The same keyword can be used for multiple folders, but this will always lead to a conflict that must be resolved manually.

If multiple keywords for multiple folders exist in the file name, the user shall be informed and be asked to confirm where the file should be relocated.

Folders will not be moved. The filter file currently in use will not be moved.