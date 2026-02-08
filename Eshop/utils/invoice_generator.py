from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def generate_invoice(invoice_path, order, order_items):
    c = canvas.Canvas(invoice_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, height - 50, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(30, height - 90, f"Order ID: {order.id}")
    c.drawString(30, height - 110, f"Customer: {order.user.username}")
    c.drawString(30, height - 130, f"Date: {order.order_date.strftime('%d-%m-%Y %H:%M')}")

    # Table Headers
    y = height - 180
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y, "Product")
    c.drawString(250, y, "Qty")
    c.drawString(320, y, "Price")
    y -= 20

    c.setFont("Helvetica", 12)
    for item in order_items:
        c.drawString(30, y, item.order_item.title)
        c.drawString(250, y, str(item.quantity))
        c.drawString(320, y, f"₹{item.price}")
        y -= 20

    # Grand Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y - 30, f"Grand Total: ₹{order.total_amount}")

    c.showPage()
    c.save()
