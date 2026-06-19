#lab13_1 (print all files in entire folder)
import os

def print_all_file_content(patH: str,tab:str) -> None:
    """
    Docstring for print_all_file_content
    
    :param patH: Description
    :type patH: str
    :param tab: Description
    :type tab: str

    DETAILS: Prints a full amount of files and folders with
    folders in it and files in it in a "beautiful way"
    """
    try:
        list_of_path = os.listdir(patH)
        list_of_path.sort()
    except PermissionError:
        print(f"{tab}└── [Access Denied]")
        return
    
    line = "|"
    last_elem = "└──"
    regular_elem = "├──"

    if not list_of_path:
        print(line, tab, last_elem, patH)

    else:
        tab += " "

        for indeX,elem in enumerate(list_of_path):
            leN = len(list_of_path)
            full_path = os.path.join(patH, elem)

            if not os.path.isdir(full_path) and indeX + 1 == leN:
                print(line,tab,last_elem,elem)
                continue
                
            if not os.path.isdir(full_path):
                print(line,tab,regular_elem,elem)

            if os.path.isdir(full_path):
                print(line,tab,regular_elem,elem)
                print_all_file_content(full_path,tab + " ")

def main():
    tab = " "
    print("c:\\TRANING")
    print_all_file_content("c:\\TRANING", tab)

if __name__ == "__main__":
    main()