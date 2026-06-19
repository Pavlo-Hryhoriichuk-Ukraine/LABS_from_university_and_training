#lab16_2 (module for cars owners)
from forcars import *

def main():
    path1 = "C:\\Users\\pavlo\\OneDrive\\LABS_PROGRAMMING\\PYTHON_LABS\\car_clear_information.txt"
    path2 = "C:\\Users\\pavlo\\OneDrive\\LABS_PROGRAMMING\\PYTHON_LABS\\binary_car_clear_information"
    number = " AB3214FD"
    new_owner = "Ivan Ilnizckiy"
    owner = "Pavlo Hryhoriichuk"
    
    write_information(input_cars(), path=path1)
    cerealizate_inf(create_dict(upload_information(path=path1)), path=path2)
    re_register_car(number,new_owner,path2)
    print_number_of_cars_of_the_same_brand(path2)
    print_info_of_cars_of_the_owner(owner,path1)

if __name__ == "__main__":
    main()