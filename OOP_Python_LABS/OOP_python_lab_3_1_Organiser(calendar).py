import json
from accessify import private, protected
from datetime import datetime, time
from  calendar import monthrange

class ValidateTime():
    """
    Data-descriptor for validation of time
    """
    def __set_name__(self, owner, name):
         self.name = "_" + name
    def __set__(self, instance, value):
        if not value:
            return
        try:
            datetime.strptime(value, "%H:%M:%S").time()
        except ValueError:
            raise ValueError("incorrect time value")
        setattr(instance, self.name, value)


class ValidateDate():
    """
    Data-descriptor for validation of date
    """
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __set__(self, instance, value):
        if not value or ":" in value:
            return
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("incorrect date value")
        setattr(instance, self.name, value)


class Organiser():
    """
    Helps you organise your daily calendar. Works only with '.json' files.
    """
    date = ValidateDate()
    start_time = ValidateTime()
    end_time = ValidateTime()

    def __init__(self, file_name):
        self._file_name = file_name

    @private
    @staticmethod
    def parse_time(time_str: str):
         return datetime.strptime(time_str, "%H:%M:%S").time()

    
    def __call__(self, date : str, start_time : str = "", end_time: str = "", main_message = "", additional_message = ""):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

        with open(self._file_name, "r") as json_file:
                file_dict = json.load(json_file)
        
        if ":" in date:
            lst_date = date.split(":")
            date_1, date_2 = datetime.strptime("1/" + lst_date[0], "%d/%m/%Y"), datetime.strptime("1/" + lst_date[1], "%d/%m/%Y")

            while date_1 <= date_2:
                dict_to_print = {}

                for day, info in file_dict.items():
                    if day.endswith(f"{date_1.month:02d}/{date_1.year}"):
                        dict_to_print[int(day[:2])] = len(info)

                proper_day, number_of_days = monthrange(date_1.year, date_1.month)

                print(f"                    {date_1.strftime("%B %Y")} ({sum(dict_to_print.values())})")
                print(f"Mon      Tue      Wed      Thu      Fri      Sat       Sun")

                print(" " * (proper_day * 9), end="")
                for day in range(1, number_of_days + 1):
                    label = f"{day}[{dict_to_print[day]}]" if day in dict_to_print else str(day)
                    print(f"{label:<9}", end="") # left alignment
                    if (proper_day + day) % 7 == 0:
                        print()

                if date_1.month == 12:
                    date_1 = date_1.replace(year=date_1.year + 1, month=1)
                else:
                    date_1 = date_1.replace(month=date_1.month + 1)
                print("\n\n")

        elif main_message:
            BASE_DICT = {
                "start_time" : start_time,
                "end_time" : end_time,
                "main_message" : main_message,
                "additional_message" : additional_message
            }
            if date not in file_dict:
                file_dict[date] = []
            file_dict[date].append(BASE_DICT)
            with open(self._file_name, "w") as json_file:
                json.dump(file_dict, json_file, indent=4)

        elif start_time and end_time:
             real_start_time = self.parse_time(start_time)
             real_end_time = self.parse_time(end_time)
             event_gen = (event for event in file_dict[date] if self.parse_time(event["start_time"]) <= real_end_time and real_start_time <= self.parse_time(event["end_time"]))
             print(*event_gen, sep="\n")

        elif start_time:
            proper_time = self.parse_time(start_time)
            lst_data = file_dict[date]
            event_gen = (event for event in lst_data if self.parse_time(event["start_time"]) <= proper_time <= self.parse_time(event["end_time"]))
            print(*event_gen, sep="\n")

        else:
            print(*file_dict[date], sep="\n")

def main():
    my_notes = Organiser(r"C:\Users\pavlo\OneDrive\LABS_PROGRAMMING\OOP_Python_LABS\organiser.json")
    my_notes(date="11/10/2025", start_time="13:11:00", end_time="15:12:00", main_message="Bidaaa")
    my_notes("10/2025:12/2025")
    
if __name__ == "__main__":
    main()
