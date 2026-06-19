#lab9_3(print a number using words)
import random

def regular_case(text:str,translator_dict: dict) -> str:
    match len(text):
        case 9:
            return translator_dict[text[0]+"00"] + " " + regular_case (text[1:], translator_dict)
        case 8:
            if text[0] == "0":
                return regular_case(text[1:],translator_dict)
            if text [0] == "1":
                return translator_dict[text[0]+text[1]] + " мільйонів " + regular_case(text[2:], translator_dict)
            return translator_dict[text[0]+"0"] + " " + regular_case (text[1:], translator_dict)

        case 7:
            to_pop = text[0]
            match int(to_pop):
                case 1:
                    adder = " мільйон "
                case 2 | 3 | 4:
                    adder = " мільйони "
                case 0:
                    adder = " мільйонів "
                    return adder + regular_case(text[1:], translator_dict)
                case _:
                    adder = " мільйонів "
                    return translator_dict[to_pop] + adder + regular_case(text[1:], translator_dict)
            return translator_dict[to_pop] + adder + regular_case(text[1:], translator_dict)
        
        case 5:
            if text[0] == "0":
               return regular_case(text[1:],translator_dict)
            if text[0] == '1':
                return  translator_dict[text[0]+text[1]]+" тисяч"+ regular_case(text[2:], translator_dict)
            if text[1] == "0":
                return translator_dict[text[0]+"0"]+" тисяч"+ regular_case(text[2:], translator_dict)
            else:
                return translator_dict[text[0]+"0"]+ regular_case(text[1:], translator_dict)
        
            
        case 6:
            if text[0] == "0":
               return regular_case(text[1:],translator_dict)
            global output
            output += translator_dict[text[0]+"00"] + " "
            if text[1] != "0" and text[1] != "1":
                output += translator_dict[text[1]+"0"]+" "+ regular_case(text[2:], translator_dict)
            elif text[1] == "1":
                output += translator_dict[text[1]+text[2]] + " тисяч" + regular_case(text[3:],translator_dict)
            elif text[1] == "0":
                 output += "тисяч"+ regular_case(text[2:], translator_dict)
            else:
                output += "тисяч " + regular_case(text[2:], translator_dict)
            return output
    
        case 4:
            if text[0] == "0":
                return regular_case(text[1:],translator_dict)
            to_pop = text[0]
            match int(to_pop):
                case 1:
                    adder = " одна тисяча"
                case 2:
                    adder = " дві тисячі"
                case 3 | 4 as cmd:
                    adder = translator_dict[f"{cmd}"] + " тисячі"
                case 5 | 6 | 7 | 8 | 9 as cmd:
                    adder = translator_dict[f"{cmd}"] + " тисяч "
            return adder + regular_case(text[1:], translator_dict)
    
        case 3 | 2 as cmd:
            if text[0] == "0":
                try:
                    return translator_dict[text[1:]]
                except KeyError:
                    if not text[2:] or text[2:] == "0":
                        return ""
                    else:
                        return translator(text[1:])
                    
            if text[1] == "0":
                    return translator(text)
            
            leN = len(text)
            output_regular = ""
            for i in range(leN):
                if text[i] == "0":
                    continue
                if text[i] == '1'and i == 1 and leN != 2:
                    output_regular += translator_dict[text[i]+text[i+1]]
                    break
                if i == 0 and leN == 3:
                    output_regular += translator_dict[text[i]+"00"] +" "
                if i == 1 and leN == 3 or i == 0 and leN == 2:
                    output_regular += translator_dict[text[i]+"0"] +" "
                if i == 2 or i == 1 and leN == 2:
                    output_regular += translator_dict[text[i]]
                    break
            return " " + output_regular
        
def translator(numbers_text: str) -> str:

    translator_dict = {"1": "один", "2": "два", "3": "три","4": "чотири",
               "5": "п'ять", "6": "шість", "7": "сім", "8": "вісім",
               "9": "дев'ять","10":"десять", "11":"одинадцять",
               "12": "дванадцять", "13": "тринадцять", "14": "чотирнадцять",
               "15": "п'ятнадцять", "16": "шістнадцять", "17" : "сімнадцять",
               "18" : "вісімнадцять", "19": "дев'ятнадцять", "20": "двадцять",
               "30": "тридцять", "40": "сорок", "50": "п'ятдесят", "60": "шістдесят",
               "70": "сімдесят", "80": "вісімдесят", "90": "дев'яносто", "100": "сто",
               "200": "двісті", "300": "триста", "400": "чотириста", "500": "п'ятсот",
               "600" : "шістсот", "700": "сімсот", "800": "вісімсот", "900": "дев'ятсот"}
    numbers_text = numbers_text.strip()
    lenght = len(numbers_text)
    global output
    output = ""
    match lenght:
        
        case 1:
            return " "+ translator_dict[numbers_text]
        
        case 2:
            if numbers_text[0] == '1':
                return translator_dict[numbers_text]
            else:
                return regular_case(numbers_text,translator_dict)
        
        case 3:
            return regular_case(numbers_text,translator_dict)
        
        case 4 | 7 | 8 | 9:
             return regular_case(numbers_text,translator_dict)
        
        case 5:
               return regular_case(numbers_text,translator_dict)
        case 6:
            if numbers_text[1] == '1' and numbers_text[1] != "0":
                return  translator_dict[numbers_text[0]+"00"] + translator_dict[numbers_text[1]+numbers_text[2]]+" тисяч"+ regular_case(numbers_text[3:], translator_dict)
            return regular_case(numbers_text, translator_dict)

number = random.randint(1,1000000000)
print(f"{number} : {translator(str(number))}")
