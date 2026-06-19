#ЗАДАЧА3

def is_strong_password(password):
    is_real_strong_password = False
    
    if len(password) >= 8:
        is_strong_password = True
    
    for simbol in password:
        if simbol == simbol.capitalize():
            is_strong_password = True
            break
        else:
            continue
    
    for simbol in password:
        if simbol != simbol.capitalize():
            is_strong_password = True
            break
        else:
            continue
    
    for simbol in password:
        if simbol is int():
            is_strong_password = True
            break
        else:
            continue

is_strong_password(input("Please, enter your own password: "))
print(is_real_strong_password)