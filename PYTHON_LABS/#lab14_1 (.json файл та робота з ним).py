#lab14_1 (.json файл і робота з ним)

import json

def json_analysis(path: str) -> None:

    def json_author_sort(author_dict:dict):
        our_list = [*author_dict["emails"],*author_dict["phones"]]
        author_dict.pop("emails")
        author_dict.pop("phones")
        author_dict["comunications"] = sorted(our_list,key=lambda elem: elem["priority"])
        return author_dict
    
    def json_language_sort(_dict_: dict) -> dict:
        _dict_["languages"] = sorted(_dict_["languages"],key=lambda elem: elem["original"],reverse=True)
        return _dict_

    
    
    with open(path, "r", encoding="utf-8") as file:
        dict_of_data = json.load(file)
    
    publications1 = dict_of_data["publications"]

    book_information = []
    article_information = []
    authors_SHORT_information = []
    authors_FULL_information = []

    for _dict_ in publications1:
        _dict_ = json_language_sort(_dict_)
        for author in _dict_["authors"]:
            author = json_author_sort(author)
            authors_FULL_information.append(author)
            authors_SHORT_information.append({"name": author["name"]})
        _dict_["authors"] = authors_SHORT_information

        match [*_dict_.keys()][0]:
            case "id":
                _dict_.pop("id")
                book_information.append(_dict_)

            case "type":
                article_information.append(_dict_)

    with open("book_information.txt", 'w',encoding="utf-8") as file:
        for book in book_information:
            file.write(f"{book}\n")
            file.write('\n')

    with open("article_information.txt", 'w',encoding="utf-8") as file:
        for article in article_information:
            file.write(f"{article}\n")
            file.write('\n')

    with open("authors_full_information.txt", 'w', encoding="utf-8") as file:
        for author in authors_FULL_information:
            file.write(f"{author}\n")
            file.write('\n')

def main():
    path = "C:\\Users\\pavlo\\Downloads\\Telegram Desktop\\publications.json"
    json_analysis(path)
    print("COMPLETED")

if __name__ == "__main__":
    main()