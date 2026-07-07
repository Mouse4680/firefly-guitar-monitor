import requests


def get_shopify_products(collection_url):
    """
    Attempts to use Shopify's JSON product endpoint.
    Returns an empty list if unavailable.
    """

    json_url = collection_url.rstrip("/") + ".json"

    try:
        response = requests.get(
            json_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("products", [])

    except Exception as e:
        print("Shopify JSON error:", e)

    return []
