#lab14_3 (re MODULE + goverment decree renaming)

import re
from string import punctuation

def edit_document(path: str) -> None:

    REGION_STRING = re.compile(r"\d{1,2}\)\s+у\s(\w+)\s(області)",re.IGNORECASE)
    with open(path,"r",encoding="utf-8") as file:
        full_clean_lst = [string.strip("\n ").strip(punctuation) for string in file.readlines()]
    
    right_lines_lst = []
    for string in full_clean_lst:
        if matcher := REGION_STRING.search(string):
            right_region = matcher.group(1)[:-2] + "а"
            right_prefix = "область"
            full_region = right_region + " " + right_prefix
            continue
        if prefix := re.search(r"(село|селище|місто|селище міського типу)",string):
            str_prefix = prefix.group(1)
            match str_prefix:
                case "село":
                    str_prefix = 'с. '
                case 'селище':
                    str_prefix = 'с-ще '
                case 'місто':
                    str_prefix = 'м. '
                case _:
                    str_prefix = 'смт. '

            right_council = right_district = ""
            #(?:) -> do not save values
            if old_title := re.search(r'(село|селище міського типу|селище|місто)\s+' 
                                  r'([А-ЯҐЄІЇа-яґєіїʼ\u2019\u0027''-]+'
                                  r'(?:\s[А-ЯҐЄІЇа-яґєіїʼ\u2019\u0027''-]+)?)'
                                  r'(?:\s+\w+ської|\s+\w+ського|\s+на\s)',
                                  string):
                right_old_title = str_prefix + old_title.group(2)

            district = re.search(r'([А-ЯИЇЮЄ][а-яюєїиʼ\u2019\u0027'']+)\s+району',string)
            if district : right_district = district.group(1)[:-3] +'ий' + ' район'

            council = re.search(r'([А-ЯИЇЮЄ][а-яюєїиʼ\u2019\u0027'']+)\s+(міської|селищної) ради',string)
            if council:
                right_council = council.group(1)[:-2] + 'a ' + council.group(2)[:-2]+'а' + ' рада'

            if new_title := re.search(
                                r'на\s+(село|селище міського типу|селище|місто)\s+'
                                r'([А-ЯҐЄІЇа-яґєіїʼ\u2019\u0027\'\-]+(?:\s[А-ЯҐЄІЇа-яґєіїʼ\u2019\u0027\'\-]+)?)',
                                string):
                right_new_title = str_prefix + new_title.group(2)
            
            if right_district and right_council:
                full_sentence = f"{full_region},{right_district},{right_old_title} {right_council}, {right_new_title}"

            elif right_council and not right_district:
                full_sentence = f"{full_region},{right_council},{right_old_title},{right_new_title}"

            elif right_district and not right_council:
                full_sentence = f"{full_region},{right_district},{right_old_title},{right_new_title}"

            else:
                full_sentence = f"{full_region},{right_old_title},{right_new_title}"
            
            right_lines_lst.append(full_sentence)

    with open("degree_new.txt","w",encoding="utf-8") as file:
                for line in sorted(right_lines_lst):
                    file.write(f"{line}\n")

def main():
    path = "C:\\Users\\pavlo\\Downloads\\Telegram Desktop\\decree.txt"
    edit_document(path)
    print("COMPLETED")

if __name__ == "__main__":
    main()