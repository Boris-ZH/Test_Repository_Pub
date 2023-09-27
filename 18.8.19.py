bil = int(input("Введите количество билетов : "))
bil_1 = bil
per = {}
price = 0
while bil > 0:
    age = int(input("Введите возраст покупателя : "))
    per[bil] = age
    bil = bil - 1
per_items = per.items()
for p, age in per_items:
    if 18 <= age <= 25:
        price = price + 990
    elif 18 > age:
        price = price + 0
    elif age > 25:
        price = price + 1390
if bil_1 > 3:
    price = price - price * 0.1
price = str(price)
print ("Итого к оплате " + (price))