from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
import os


def generate_invoice(invoice_path, order, order_items):

    c = canvas.Canvas(invoice_path, pagesize=A4)
    width, height = A4

    # ======================================================
    #                HEADER - SHOP DETAILS
    # ======================================================
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30, height - 50, "BEAST ARMS & AMMUNITIONS")

    c.setFont("Helvetica", 10)
    c.drawString(30, height - 70, "High Grade Arms | Tactical Gear | Licensed Products")
    c.drawString(30, height - 85, "Email: support@beastarms.com | Phone: +91 90000 00000")

    # Line under header
    c.line(30, height - 95, width - 30, height - 95)

    # ======================================================
    #                 INVOICE TITLE + ORDER INFO
    # ======================================================
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, height - 125, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(30, height - 155, f"Invoice No: {order.id}")
    c.drawString(30, height - 175, f"Date: {order.order_date.strftime('%d-%m-%Y %H:%M')}")

    # ======================================================
    #                  CUSTOMER DETAILS
    # ======================================================
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 210, "Customer Details")

    c.setFont("Helvetica", 11)
    c.drawString(30, height - 230, f"Name: {order.user.username}")

    # OPTIONAL — If you have address fields:
    try:
        c.drawString(30, height - 250, f"Address: {order.address.address_line}")
        c.drawString(30, height - 270, f"City: {order.address.city}")
        c.drawString(30, height - 290, f"Phone: {order.address.phone}")
    except:
        c.drawString(30, height - 250, "Address: N/A")

    # ======================================================
    #                 PRODUCT TABLE HEADERS
    # ======================================================
    y = height - 330

    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y, "Product")
    c.drawString(240, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(380, y, "Image")

    c.line(30, y - 5, width - 30, y - 5)
    y -= 30

    # ======================================================
    #                PRODUCT TABLE ROWS
    # ======================================================
    c.setFont("Helvetica", 11)

    for item in order_items:

        # Product name
        c.drawString(30, y, item.order_item.title[:35])

        # Qty
        c.drawString(240, y, str(item.quantity))

        # Price
        c.drawString(300, y, f"₹{item.price}")

        # Product Image
        try:
            img_path = item.order_item.thumbnail.path
            if os.path.exists(img_path):
                c.drawImage(ImageReader(img_path), 380, y - 15, width=40, height=40, mask='auto')
            else:
                c.drawString(380, y, "No Image")
        except:
            c.drawString(380, y, "No Image")

        y -= 50

        if y < 120:
            c.showPage()
            y = height - 100

    # ======================================================
    #                PRICE SUMMARY BOX
    # ======================================================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y - 20, "Subtotal:")
    c.drawString(150, y - 20, f"₹{order.total_amount}")

    delivery_charge = 0
    gst = round(order.total_amount * 0.12)

    c.drawString(30, y - 40, "Delivery Charge:")
    c.drawString(150, y - 40, f"₹{delivery_charge}")

    c.drawString(30, y - 60, "GST (12%):")
    c.drawString(150, y - 60, f"₹{gst}")

    # Grand Total
    grand_total = order.total_amount + delivery_charge + gst

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y - 90, f"Grand Total: ₹{grand_total}")
    c.line(30, y - 95, 200, y - 95)

    # ======================================================
    #                 PAID / UNPAID STAMP
    # ======================================================
    c.setFont("Helvetica-Bold", 40)
    if order.status == "PAID":
        c.setFillColorRGB(0, 0.6, 0)
        c.drawString(350, y - 20, "PAID")
    else:
        c.setFillColorRGB(0.8, 0, 0)
        c.drawString(330, y - 20, "UNPAID")

    c.setFillColorRGB(0, 0, 0)

    # ======================================================
    #                 FOOTER
    # ======================================================
    c.setFont("Helvetica", 10)
    c.drawString(30, 40, "Thank you for shopping with Beast Arms.")
    c.drawString(30, 25, "This invoice is system-generated and does not require signature.")

    c.showPage()
    c.save()
