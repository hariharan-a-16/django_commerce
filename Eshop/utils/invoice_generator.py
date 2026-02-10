from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from decimal import Decimal, ROUND_HALF_UP
import os


def generate_invoice(invoice_path, order, order_items):

    c = canvas.Canvas(invoice_path, pagesize=A4)
    width, height = A4

    LEFT = 30      # left margin
    RIGHT = width - 30
    y = height - 50

    # ======================================================
    #                HEADER - SHOP DETAILS
    # ======================================================
    c.setFont("Helvetica-Bold", 22)
    c.drawString(LEFT, y, "STYLOO JERSEY SHOP")

    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(LEFT, y, "Premium Jerseys | Stylish Apparel | Trusted Quality")
    y -= 15
    c.drawString(LEFT, y, "Email: support@styloo.com | Phone: +91 90000 00000")

    y -= 15
    c.line(LEFT, y, RIGHT, y)

    # ======================================================
    #                INVOICE + ORDER INFO
    # ======================================================
    y -= 40
    c.setFont("Helvetica-Bold", 18)
    c.drawString(LEFT, y, "INVOICE")

    # Order Info
    c.setFont("Helvetica", 11)
    y -= 30
    c.drawString(LEFT, y, f"Invoice No: {order.id}")
    y -= 20
    c.drawString(LEFT, y, f"Date: {order.order_date.strftime('%d-%m-%Y %H:%M')}")

    # ======================================================
    #                CUSTOMER DETAILS
    # ======================================================
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(LEFT, y, "Customer Details")

    c.setFont("Helvetica", 11)
    y -= 20
    c.drawString(LEFT, y, f"Name: {order.user.username}")

    try:
        y -= 20
        c.drawString(LEFT, y, f"Address: {order.address.address_line}")
        y -= 20
        c.drawString(LEFT, y, f"City: {order.address.city}")
        y -= 20
        c.drawString(LEFT, y, f"Phone: {order.address.phone}")
    except:
        y -= 20
        c.drawString(LEFT, y, "Address: N/A")

    # ======================================================
    #                PRODUCT TABLE HEADER
    # ======================================================
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, y, "Product")
    c.drawString(260, y, "Qty")
    c.drawString(320, y, "Price")
    c.drawString(400, y, "Image")

    y -= 10
    c.line(LEFT, y, RIGHT, y)
    y -= 25

    # ======================================================
    #                PRODUCT TABLE ROWS
    # ======================================================
    c.setFont("Helvetica", 11)

    for item in order_items:

        c.drawString(LEFT, y, item.order_item.title[:40])
        c.drawString(260, y, str(item.quantity))
        c.drawString(320, y, f"₹{item.price}")

        try:
            img_path = item.order_item.thumbnail.path
            if os.path.exists(img_path):
                c.drawImage(ImageReader(img_path), 400, y - 15, width=35, height=35)
        except:
            c.drawString(400, y, "No Image")

        y -= 50

        if y < 150:
            c.showPage()
            y = height - 100

    # ======================================================
    #                PRICE SUMMARY (Right aligned)
    # ======================================================
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, y, "Subtotal:")
    c.drawRightString(RIGHT, y, f"₹{order.total_amount}")

    delivery_charge = Decimal("0.00")
    gst_rate = Decimal("0.12")
    gst = (order.total_amount * gst_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    y -= 20
    c.drawString(LEFT, y, "Delivery Charge:")
    c.drawRightString(RIGHT, y, f"₹{delivery_charge}")

    y -= 20
    c.drawString(LEFT, y, "GST (12%):")
    c.drawRightString(RIGHT, y, f"₹{gst}")

    # Grand Total
    grand_total = (order.total_amount + delivery_charge + gst).quantize(Decimal("0.01"))

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(LEFT, y, "Grand Total:")
    c.drawRightString(RIGHT, y, f"₹{grand_total}")

    c.line(LEFT, y - 5, RIGHT, y - 5)

    # ======================================================
    #                PAID / UNPAID (Top Right)
    # ======================================================
    c.setFont("Helvetica-Bold", 34)

    status = order.status.upper()   # convert to uppercase

# Treat these as PAID
    paid_statuses = ["PAID", "COMPLETED", "SUCCESS"]

    if status in paid_statuses:
        c.setFillColorRGB(0, 0.6, 0)
        c.drawRightString(RIGHT, height - 140, "PAID")
    else:
        c.setFillColorRGB(0.8, 0, 0)
        c.drawRightString(RIGHT, height - 140, "UNPAID")

    c.setFillColorRGB(0, 0, 0)

    # ======================================================
    #                FOOTER
    # ======================================================
    c.setFont("Helvetica", 10)
    c.drawString(LEFT, 40, "Thank you for shopping with Styloo.")
    c.drawString(LEFT, 25, "This invoice is auto-generated and requires no signature.")

    c.showPage()
    c.save()
