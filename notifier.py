import smtplib

from email.message import EmailMessage

from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    TO_EMAIL
)


def send_email(products):

    if not products:
        return


    html = """
    <html>
    <body>
    <h1>🎸 New Firefly Guitar Alert!</h1>
    """


    for product in products:

        image = product.get("image", "")

        html += f"""
        <hr>

        <h2>{product['title']}</h2>

        <p>
        Collection:
        {product['collection']}
        </p>

        <p>
        Price:
        {product.get('price','Unknown')}
        </p>

        <img src="{image}" width="300">

        <br><br>

        <a href="{product['url']}">
        View Guitar
        </a>

        """

    html += """
    </body>
    </html>
    """


    msg = EmailMessage()

    msg["Subject"] = (
        "🎸 New Firefly Guitar Added!"
    )

    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL


    msg.set_content(
        "New Firefly guitar detected."
    )


    msg.add_alternative(
        html,
        subtype="html"
    )


    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)
