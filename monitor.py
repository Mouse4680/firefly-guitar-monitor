import requests
from bs4 import BeautifulSoup

from config import COLLECTIONS
from state import load_state, save_state
from notifier import send_email
from shopify import get_shopify_products


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def parse_shopify_products(products, collection):

    results = {}

    for product in products:

        title = product.get("title")

        handle = product.get("handle")

        if not title or not handle:
            continue


        url = (
            "https://guitarsgarden.com/products/"
            + handle
        )


        variants = product.get(
            "variants",
            []
        )


        price = "Unknown"
        available = False


        if variants:

            price = (
                variants[0]
                .get("price", "Unknown")
            )

            available = any(
                v.get("available", False)
                for v in variants
            )


        image = ""

        images = product.get(
            "images",
            []
        )

        if images:
            image = images[0].get(
                "src",
                ""
            )


        results[url] = {

            "title": title,

            "collection": collection,

            "url": url,

            "price": price,

            "available": available,

            "image": image
        }


    return results



def scrape_html_collection(
        collection,
        url
):

    products = {}

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        for link in soup.select(
            "a[href*='/products/']"
        ):

            href = link.get(
                "href"
            )


            title = link.get_text(
                strip=True
            )


            if not href or not title:
                continue


            if href.startswith("/"):
                href = (
                    "https://guitarsgarden.com"
                    + href
                )


            products[href] = {

                "title": title,

                "collection": collection,

                "url": href,

                "price": "Unknown",

                "available": True,

                "image": ""
            }


    except Exception as e:

        print(
            "HTML error:",
            e
        )


    return products



def get_all_products():

    all_products = {}


    for collection, url in COLLECTIONS.items():

        print(
            "Checking:",
            collection
        )


        products = get_shopify_products(
            url
        )


        if products:

            parsed = parse_shopify_products(
                products,
                collection
            )

        else:

            print(
                "Using HTML fallback"
            )

            parsed = scrape_html_collection(
                collection,
                url
            )


        all_products.update(
            parsed
        )


    return all_products



def compare_products(
        old,
        new
):

    alerts = []


    for url, product in new.items():

        # Brand new guitar

        if url not in old:

            alerts.append(product)

            continue



        previous = old[url]


        # Restock detection

        if (
            previous.get("available")
            == False

            and

            product.get("available")
            == True
        ):

            product["alert"] = (
                "RESTOCK"
            )

            alerts.append(product)



        # Price change detection

        if (
            previous.get("price")
            != product.get("price")
        ):

            product["alert"] = (
                "PRICE CHANGE"
            )

            alerts.append(product)


    return alerts



def main():

    print(
        "Starting Firefly monitor..."
    )


    old_products = load_state()


    current_products = (
        get_all_products()
    )


    alerts = compare_products(
        old_products,
        current_products
    )


    if alerts:

        print(
            "Changes found:",
            len(alerts)
        )


        send_email(
            alerts
        )

    else:

        print(
            "No changes detected."
        )


    save_state(
        current_products
    )



if __name__ == "__main__":

    main()
