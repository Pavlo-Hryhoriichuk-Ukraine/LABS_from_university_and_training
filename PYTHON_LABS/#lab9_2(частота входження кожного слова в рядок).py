#lab9_2(частота входження кожного слова в рядок)

def text_cleaning(text:str) -> str:
    for char in text:
        if not char.isalpha() and char not in ("-","`"):
            text = text.replace(char, " ")
    return text

def word_counting(cleaned_text:str) -> dict[str,float]:
    list_of_words = cleaned_text.split()
    length_of_list = len(list_of_words)
    dict_of_words = {}

    for word in list_of_words:
        if word.lower() not in dict_of_words:
            dict_of_words[word] = float(round(list_of_words.count(word)/length_of_list), 2)
    return dict_of_words

def main():
    text = input("Input your text: ")
    print(word_counting(text_cleaning(text)))

if __name__ == "__main__":
    main()