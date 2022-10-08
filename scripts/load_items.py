import csv
from decimal import Decimal

from catalog.models import *


def gen_categories(cat: str):
    categories = cat.split("/")

    if Category.objects.filter(name=categories[0]).exists():
        return Category.objects.filter(name=categories[0]).first()
    return Category.objects.create(name=categories[0])


def get_vendor(ven: str):
    vendor_in = ven.strip()

    if Vendor.objects.filter(name=vendor_in).exists():
        return Vendor.objects.filter(name=vendor_in).first()
    else:
        return Vendor.objects.create(name=vendor_in)


def get_old_price(op):
    if op:
        try:
            oldprice = Decimal(op)
            return oldprice
        except:
            return None
    return None


def run():
    with open('catalog/products.csv', encoding="utf8") as file:
        reader = csv.reader(file, delimiter=";", )
        next(reader)

        Product.objects.all().delete()
        Vendor.objects.all().delete()
        Category.objects.all().delete()

        for row in reader:
            item = Product(
                prod_id=row[13],
                code=row[2],
                name=row[9],
                description=row[5],
                picture=row[11],
                guarantee=row[6],
                stock=row[13],
                redirect_url=row[-2],
                oldprice=get_old_price(row[10]),
                price=get_old_price(row[12]),
                merchant=Merchant.objects.get(pk=1),
                vendor=get_vendor(row[-1]),
                category=gen_categories(row[1])
            )

            item.save()
