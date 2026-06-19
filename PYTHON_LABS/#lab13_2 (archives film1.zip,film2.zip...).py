#lab13_2 (archives film1.zip,film2.zip...)
import os
import zipfile 
import tempfile
import csv
import re
import doctest

def get_dict_of_paths(*args: tuple[str]) -> dict[str,list]:
    """
    Docstring for get_dict_of_paths
    
    :param args: Description
    :type args: tuple[str]
    :return: Description
    :rtype: dict[str, list]
    DETAILS: Gets dict of paths of files you inputted, value is a list of
    different pathes of the same object in your OS.
    """
    dict_of_paths = {file.lower() : [] for file in args}
    gen = os.walk("c:\\")
    try: #
        while True:
            try:
                while True:
                    g = next(gen)
                    root,forders,files = g
                    for file in files:
                        if file.lower() in dict_of_paths:
                            dict_of_paths[file].append(root)
            except PermissionError:
                while True:
                    g = next(gen)
                    for root,forders,files in g:
                        for file in files:
                            if file.lower() in dict_of_paths:
                                dict_of_paths[file].append(root)

    except StopIteration:
        return dict_of_paths

def unarchive_and_unite_file_in_txt_format_in_archive(dict_of_files: dict[str,list[str]]) -> str:
                    """
                    Docstring for unarchive_and_unite_file_in_txt_format_in_archive
                    
                    :param dict_of_files: Description
                    :type dict_of_files: dict[str, list[str]]
                    :return: Description
                    :rtype: str
                    DETAILS: Hepls you unarchive file from dict of files from past function, and unite all
                    .csv and .txt files texts in one new .txt file
                    """
                    
                    with open("film.txt", "w", encoding="utf-8") as new_file:
                        unique_lines = []
                        seen_lines = set()
                        for zipped, directions in dict_of_files.items():
                                source_zip = os.path.join(directions[0],zipped)

                                with tempfile.TemporaryDirectory() as tempdir:
                                    with zipfile.ZipFile(source_zip, 'r') as z:
                                        z.extractall(tempdir)
                                    for root, _, files in os.walk(tempdir):
                                        for file in files:

                                            if file.endswith('.txt'):
                                                file_path = os.path.join(root, file)
                                                with open(file_path, "r", encoding="utf-8") as reader:
                                                    for line in reader:
                                                        clean_low_line = line.strip()
                                                        if clean_low_line not in seen_lines:
                                                            unique_lines.append(clean_low_line)
                                                            seen_lines.add(clean_low_line)

                                            if file.endswith(".csv"):
                                                file_path = os.path.join(root, file)

                                                with open(file_path, encoding="utf-8") as csvfile:
                                                    reader = csv.reader(csvfile, delimiter=';')
                                                    
                                                    for list_line in reader:
                                                        clean_low_line = " ".join(list_line).strip()
                                                        if clean_low_line not in seen_lines:
                                                            unique_lines.append(clean_low_line)
                                                            seen_lines.add(clean_low_line)

                        for line in unique_lines:
                            new_file.write(line + "\n")
                        return "film.txt"
                    
def list_of_file_writed_lines(path:str) -> list[list[str]]:
     """
     Docstring for list_of_file_writed_lines
     
     :param path: Description
     :type path: str
     :return: Description
     :rtype: list[list[str]]
     DETAILS: Reads file and returns to you list of lists, where you
     can find each of line in file you have written.
     """
     with open(path,"r",encoding="utf-8") as film_file:
          list_of_films = []
          for line in film_file:
               list_of_films.append([line.strip()])
          return list_of_films
          
def get_film_rating(lst:list[list[str]], n:int) -> list[tuple[str,str]]:
     """
     Docstring for get_film_rating
     
     :param lst: Description
     :type lst: list[list[str]]
     :param n: Description
     :type n: int
     :return: Description
     :rtype: tuple[str, str]
     DETAILS: Creates a list of tuples of films (max amount of allowed films == n-inputed number)
     , that includes a film title and rating. Sorted in descending order.
     """
     trimmed_list_to_sort = lst[1:n+1]
     #elem[0]... -> title
     list_to_sort = [(elem[0].split("\t")[1], "".join(re.findall(r"\b[0-9]\.[0-9]\b",elem[0]))) for elem in trimmed_list_to_sort]
     sorted_list = sorted(list_to_sort,key=lambda elem: float(elem[1]),reverse=True)
     return sorted_list

def film_genre_count(list_of_films: list[list[str]]) -> dict[str,int]:
    """
    Docstring for film_genre_count
    
    :param list_of_films: Description
    :type list_of_films: list[list[str]]
    :return: Description
    :rtype: dict[str, int]
    DETAILS: Finds all genres in films, counts it and writes into a dict. 

    >>> sorted(list(film_genre_count(list_of_file_writed_lines("film.txt")).items()))[:3]
    [('Action', 303), ('Adventure', 259), ('Animation', 49)]"""

    dict_of_genre = {}
    for elem in list_of_films[1:]:
        try:
            list_of_genres = "".join(elem).split("\t")[2].split(",")

            match len(list_of_genres):
                case 1:
                        genre = "".join(list_of_genres)
                        if genre.isdigit():
                             continue
                        if genre not in dict_of_genre:
                            dict_of_genre[genre] = 1
                        else:
                            dict_of_genre[genre] += 1
                case _:
                    for genre in list_of_genres:
                                if genre.isdigit():
                                    continue
                                if genre not in dict_of_genre:
                                    dict_of_genre[genre] = 1
                                else:
                                    dict_of_genre[genre] += 1
        except:
            continue
        
    return dict_of_genre

def write_dict_into_file(dict_of_genre: dict[str,int],write_to_file_name:str= "completed_dict.txt"):
     """
     Docstring for write_dict_into_file
     
     :param dict_of_genre: Description
     :type dict_of_genre: dict[str, int]
     :param write_to_file_name: Description
     :type write_to_file_name: str
     DETAILS: Finally, writes into a new file our dict of geners in a propper way.
     """
     with open(write_to_file_name,"w",encoding="utf-8") as file:
          for key, value in dict_of_genre.items():
               file.write(f"{key} -> {value}\n")

def main():
    write_dict_into_file(film_genre_count(list_of_file_writed_lines(unarchive_and_unite_file_in_txt_format_in_archive(get_dict_of_paths("films1.zip","films2.zip","films3.zip")))))
    print(get_film_rating(list_of_file_writed_lines("film.txt"),10))
    
    with open("completed_dict.txt", "r", encoding="utf-8") as file:
         for line in file:
              print(file.read())
         file.seek()

if __name__ == "__main__":
     doctest.testmod(verbose=True)
     main()