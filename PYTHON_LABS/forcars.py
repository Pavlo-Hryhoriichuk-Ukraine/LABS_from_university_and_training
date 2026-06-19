import re
import pickle

def input_cars() -> list[str]:
    """
    Return clear list of inputed cars
    """
    #user_input = input("Input information about car or cars: ")
    user_input = "Mersedes-Benz, AB3214FD, 2023, Pavlo Hryhoriichuk; Honda, DR4215KH, 2003, Josef Tadani; Lamborgini, EQ5215KJ, 2020, Octopus Vogon; Kia, TY8459JU, 2017, Pavlo Hryhoriichuk"
    lst_of_cars = user_input.split(";")
    print(lst_of_cars)
    return lst_of_cars

def write_information(lst_of_cars: list[str], path: str) -> None:
    """
    Write info from our list to a proper file
    """
    with open(path, "w", encoding="utf-8") as file:
        for car in lst_of_cars:
            file.write(f"{car}\n")

def upload_information(path:str) -> list[str] | TypeError:
    """
    Show to you full contents of file and return list.
    """
    lst_of_cars = []
    try:
        with open(path, "r",encoding="utf-8") as file:
            for line in file:
                lst_of_cars.append(line)
            print(lst_of_cars)
            return lst_of_cars
    except FileNotFoundError:
        raise TypeError("This file does not exist!")


def create_dict(lst_of_cars: list[str]) -> dict[str,list[str]]:
    dict_of_cars = {}
    for car in lst_of_cars:
        if number := re.search(r"\s*[A-Z]{2}\d{4}[A-Z]{2}\s*",car):
            dict_of_cars[number.group(0)] = car.replace(f"{number.group(0)},","").split(",")
    print(dict_of_cars)
    return dict_of_cars

def cerealizate_inf(dict_of_cars: dict[str,list[str]], path:str) -> None:
      with open(path, "wb") as file:
          pickle.dump(dict_of_cars, file)

def decerealizate_inf(path:str) -> dict[str,list[str]] | TypeError:
    try:
        with open(path, "rb") as file:
            dict_of_cars = pickle.load(file)
            print(dict_of_cars)
            return dict_of_cars
    except FileNotFoundError:
        raise TypeError("This file does not exist!")

def re_register_car(number: str, new_owner:str, path: str) -> None | TypeError:
    dict_of_cars = decerealizate_inf(path=path)

    try:
        lst = dict_of_cars[number]
        string = ",".join(lst)
        print(string)
        old_owner = re.search(r"[A-ZА-ЯЇЄЮ][a-zа-яїюєи]+\s+[A-ZА-ЯЇЄЮ][a-zа-яїюєи]+", string)
        old_owner = old_owner.group(0)
        string = string.replace(old_owner,f"{new_owner}\n")
        dict_of_cars[number] = string.split(",")
        cerealizate_inf(dict_of_cars,path)
        print("Replacement has been done successfully")

    except KeyError:
        raise TypeError("We cannot find such an number in the database")

def print_number_of_cars_of_the_same_brand(path: str) -> None:
    dict_of_cars = decerealizate_inf(path=path)
    lst_of_brands = []
    for lst in dict_of_cars.values():
        #lst_of_brands = list(filter(lambda elem: re.fullmatch(r"[A-ZА-ЯЇЄЮ][a-zа-яїюєи]+\-*[A-ZА-ЯЇЄЮ][a-zа-яїюєи]*",elem), lst))
        print("".join(lst))
        car_brand = re.search(r"\s*[A-ZА-ЯЇЄЮ][a-zа-яїюєи]+[-]*[A-ZА-ЯЇЄЮ]*[a-zа-яїюєи]*\s*", "".join(lst))
        lst_of_brands.append(car_brand.group(0))

    dict_of_brands = {}
    for brand in lst_of_brands:
        dict_of_brands[brand] = lst_of_brands.count(brand)
    print(dict_of_brands)

def print_info_of_cars_of_the_owner(owner: str, path: str) -> None:
    lst_of_cars = upload_information(path)
    lst_of_edited_cars = [car.replace(f"{owner}\n", "") for car in lst_of_cars if owner in car]
    print(f"{owner}: {lst_of_edited_cars}")