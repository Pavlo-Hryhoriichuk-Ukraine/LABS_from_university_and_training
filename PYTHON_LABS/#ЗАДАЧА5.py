#ЗАДАЧА5

purchases = [
    {"name": "сир", "category": "їжа", "price": 120},
    {"name": "шампунь", "category": "гігієна", "price": 85},
    {"name": "хліб", "category": "їжа", "price": 35},
    {"name": "вино", "category": "їжа", "price": 210},
]


def analyze_spending(purchases, max_price = 200):
    for purchase in purchases:
        total_price = 0
        first_category = purchases[1]['category']
        if 'category' == first_category:
            'price'+= total_price
        else:
            continue
     
        
        if total_price <= max_price:
           for purchase in purchases:
                total_price = 0
                first_category = purchases[1+=1]['category']
                if 'category' == first_category:
                    'price'+= total_price
                else:
                    continue
        else:
            break

        if total_price <= max_price:
           for purchase in purchases:
                total_price = 0
                first_category = purchases[1+=1]['category']
                if 'category' == first_category:
                    'price'+= total_price
                else:
                    continue
        else:
            break

        if total_price <= max_price:
           for purchase in purchases:
                total_price = 0
                first_category = purchases[1+=1]['category']
                if 'category' == first_category:
                    'price'+= total_price
                else:
                    continue
        else:
            break
print("{['category']} is overspend}")

overspent = analyze_spending
print(overspent)
