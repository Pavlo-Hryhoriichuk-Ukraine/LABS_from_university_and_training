#lab14_2(class Validator +re MODULE)
import re

class Validator:
    
    def validate_name_surname(self, name: str) -> bool:
       matcher = re.fullmatch(r"[A-Z]{1}[a-z]{1,29}\s[A-Z][a-z]{1,29}",name.strip())
       return True if matcher else False
           
    def validate_age(self, age: str) -> bool:
        matcher = re.fullmatch(r"[0-9]{2}",age.strip())
        return False if not 16 <= int(matcher.group(0)) <= 99 else True
    
    def validate_country(self, country: str) -> bool:
       matcher = re.fullmatch(r"[A-Z]{1}[a-zA-Z]{1,9}",country.strip())
       return True if matcher else False
        
    def validate_region(self, region: str) -> bool:
        matcher = re.fullmatch(r"[A-Z0-9]{1}[a-zA-Z0-9]{1,9}",region.strip())
        return True if matcher else False

    def validate_living_place(self, place: str) -> bool:
        matcher = re.fullmatch(r"[A-Z][a-z]{2,19}\s+(st\.|av\.|prosp\.|rd\.)\s+\d\w",place.strip())
        return True if matcher else False
        # match matcher:
        #     case None:
        #         return False
        #     case _:
        #         return True
    
    def validate_index(self, index: str) -> bool:
        matcher = re.fullmatch(r"\d{5}",index.strip())
        return True if matcher else False
    
    def validate_phone(self, phone: str) -> bool:
        matcher = re.fullmatch(r"\+\d{1,2}\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}",phone.strip())
        return True if matcher else False
    
    def validate_email(self, email: str) -> bool:
        matcher = re.fullmatch(r"[^\.].{1,63}@[a-z\.]{1,255}(com|org|edu|gov|net|ua)?\.(com|org|edu|gov|net|ua)",email.strip())
        return True if matcher else False
    
    def validate_id(self, ident: str) -> bool:
        matcher = re.fullmatch(r"\d{6}",ident.strip())
        return False if not matcher.group(0).count("0") == 1 <= 99 else True
                   
    
    def validate(self, string: str) -> bool:
        if ";" in string:
            lst = string.split(";")
        else:
            lst = string.split(",")

        try:
            assert self.validate_name_surname(lst[0]) is True
            assert self.validate_age(lst[1]) is True
            assert self.validate_country(lst[2]) is True
            assert self.validate_region(lst[3]) is True
            assert self.validate_living_place(lst[4]) is True
            assert self.validate_index(lst[5]) is True
            assert self.validate_phone(lst[6]) is True
            assert self.validate_email(lst[7]) is True
            assert self.validate_id(lst[8]) is True

        except AssertionError:
            print("Not valid.")
        else:
            print("Valid.")
            return True

if __name__ == '__main__':
    valid = Validator()
    assert valid.validate("Elvis Presley,20,Ukraine, Lviv, Drahomanova st. 12,79000,+380951234567,username@domain.com,123450") is True
    assert valid.validate("Elvis Presley;20;Ukraine; Lviv;Drahomanova st. 12;79000;+380951234567;username@domain.com;123450") is True
    assert valid.validate("Elvis Presley; 20; Ukraine; Lviv; Drahomanova st. 12; 79000; +380951234567; username@domain.com; 123450") is True
    assert valid.validate("Elvis Presley, 20, Ukraine, Lviv, Drahomanova st. 12, 79000, +380951234567, username@domain.com, 123450") is True