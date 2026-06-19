from typing import Callable

def weekday_order(lst_of_weekdays: list[str]) -> list[str]:
    weekdays_dict = {
                "Monday" : 1,
                "Tuesday" : 2,
                "Wednesday" : 3,
                "Thursady" : 4,
                "Friday": 5,
                "Saturday" : 6,
                "Sunday" : 7
                }
    return sorted(lst_of_weekdays, key=lambda day: weekdays_dict[day])

def sort_weekdays(lst_of_weekdays: list[str], sort_key : Callable[[list[str]], list[str]] = weekday_order) -> list[str]:
    return sort_key(lst_of_weekdays)

if __name__ == "__main__":
    our_lst = ["Saturday", "Tuesday", "Friday", "Monday"]
    print(sort_weekdays(our_lst))