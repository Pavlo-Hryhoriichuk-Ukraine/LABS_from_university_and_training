#ЗАДАЧА4

price_limit = 50

products = [
    {"name": "Молоко", "price": 35},
    {"name": "Хліб", "price": 25},
    {"name": "Сир", "price": 80},
    {"name": "Йогурт", "price": 40},
    {"name": "Кава", "price": 120}
]

affordable_products = []

def filter_expensive_products(products):
    for product in products:
        if product ["price"] < price_limit:
            affordable_products.append(product)

filter_expensive_products(products)
        
print(f"Список доступних товарів: \n {affordable_products}") 