from django.core.mail import EmailMessage
from django.conf import settings

import io
import csv

from .models import ProductSold


def log_generator(request):
    email = request.user.email
    data = request.data

    product_id = data.get('product_id', None)
    seller_id = data.get('seller_id', None)
    date_from = data.get('date_from', None)
    date_to = data.get('date_to', None)

    producs_sold = ProductSold.objects.all()

    if product_id:
        producs_sold = producs_sold.filter(product__id=product_id)

    if seller_id:
        producs_sold = producs_sold.filter(seller__id=seller_id)

    if date_from:
        producs_sold = producs_sold.filter(created_at__exact=date_from)

    if date_from and date_to:
        producs_sold = producs_sold.filter(created_at__range=[date_from, date_to])

    create_log_report(producs_sold, email)


def create_log_report(producs_sold, email):
    filename = 'report.csv'

    data = io.StringIO()
    spamwriter = csv.writer(data)
    spamwriter.writerow(('Product', 'Price', 'Seller', 'Client', 'date', 'time'))

    for product_sold in producs_sold:
        Product = product_sold.product.name
        Price = product_sold.product.price
        Seller = product_sold.seller.user.name
        Client = product_sold.client.user.name
        date = product_sold.created_at.strftime("%Y/%m/%d")
        time = product_sold.created_at.strftime("%H:%M:%S")

        spamwriter.writerow((Product, Price, Seller, Client, date, time))

    if email:
        send_email_report(email, data.getvalue(), filename)


def send_email_report(email, report, file):
    msg = EmailMessage(
        u'Logs',
        '<br>Products sold: <br>',
        to=[email, ],
        from_email=settings.EMAIL_HOST_USER,
        attachments=[(file, report)]
    )
    msg.content_subtype = 'html'
    msg.send()
