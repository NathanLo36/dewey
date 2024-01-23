# dewey
Simple File Sorting

Takes files and sorts them into folders by file name.

Filters are stored in plain text in the `filters.txt` file like this:

    keyword|||folder
    keyword2|||folder2
    keyword3,keyword4|||folder3

Folders are stored as absolute directories.

Such that if the keyword is in the file name, it will be designated to be put into the corresponding folder. Multiple keywords can exist for the same folder. Special characters can be used in keywords, except for these:

    ,/\ 

Using `|||` in a keyword or a folder name is also not allowed.

File extensions will not be considered when sorting. In a file named like `name.log.txt`, the `.log` will be considered, but the `.txt` will not.

If multiple keywords for multiple folders exist in the file name, the user shall be informed and be asked to confirm where the file should be relocated.

Folders will not be moved.