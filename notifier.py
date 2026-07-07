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

        html += f"""

        <hr>

        <h2>{product['title']}</h2>

        <p>
        Collection:
        {product['collection']}
        </p>

        <p>
        Alert:
        {product.get('alert','NEW GUITAR')}
        </p>

        <p>
        Price:
        {product.get('price','Unknown')}
        </p>

        <a href="{product['url']}">
        View Guitar
        </a>

        <br><br>

        """

    html += """

    </body>
    </html>

    """


    msg = EmailMessage()

    msg["Subject"] = (
        "🎸 Firefly Guitar Alert"
    )

    msg["From"] = EMAIL_ADDRESS

    msg["To"] = TO_EMAIL


    msg.set_content(
        "A new Firefly guitar event was detected."
    )


    msg.add_alternative(
        html,
        subtype="html"
    )


    # Yahoo SMTP settings

    with smtplib.SMTP_SSL(
        "smtp.mail.yahoo.com",
        465
    ) as server:

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)
