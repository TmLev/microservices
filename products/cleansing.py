# coding=utf-8

import pandas as pd
from lxml import etree as ET


def get_clean_products():
    df = pd.read_csv("raw_amazon_products.csv")

    df = df.drop(
        columns=[
            "manufacturer", "price", "number_available_in_stock",
            "number_of_reviews", "number_of_answered_questions",
            "average_review_rating", "customers_who_bought_this_item_also_bought",
            "description", "product_information", "product_description",
            "items_customers_buy_after_viewing_this_item",
            "customer_questions_and_answers", "customer_reviews", "sellers",
        ],
    )

    df = df.rename(
        columns={
            "uniq_id":                          "id",
            "product_name":                     "title",
            "amazon_category_and_sub_category": "category",
        },
    )

    df = df.dropna()

    return df


def save_to_csv(df):
    df.to_csv("products.csv", index=False)


def save_to_xml(df):
    products = ET.Element("products")

    for index, row in df.iterrows():
        product = ET.SubElement(products, "product")

        id_ = ET.SubElement(product, "id")
        id_.text = row.id

        title = ET.SubElement(product, "title")
        title.text = row.title

        category = ET.SubElement(product, "category")
        category.text = row.category

    tree = ET.ElementTree(products)
    tree.write("products.xml", pretty_print=True)


def main():
    products = get_clean_products()
    save_to_csv(products)
    save_to_xml(products)


if __name__ == "__main__":
    main()
