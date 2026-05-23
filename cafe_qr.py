import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import datetime
import random

# ---------------- MAIN WINDOW ---------------- #

root = tk.Tk()
root.title("Restaurant POS System")
root.geometry("1000x750")
root.resizable(True, True)
root.config(bg="#f5f5f5")
# ---------------- MENU ITEMS ---------------- #

menu_items = {
    "Veg Burger": 120,
    "Cheese Burger": 150,
    "Chicken Burger": 180,
    "Margherita Pizza": 220,
    "Veg Pizza": 250,
    "White Sauce Pasta": 180,
    "French Fries": 90,
    "Cold Coffee": 110,
    "Coke": 60
}

# ---------------- VARIABLES ---------------- #

customer_name = tk.StringVar()
table_number = tk.StringVar()
bill_number = tk.StringVar()

order_quantities = {}

for item in menu_items:
    order_quantities[item] = tk.IntVar()

# ---------------- GENERATE BILL NUMBER ---------------- #

def generate_bill_no():

    random_bill = random.randint(1000, 9999)

    bill_number.set(str(random_bill))

    messagebox.showinfo(
        "Bill Number",
        f"Generated Bill No: {random_bill}"
    )

# ---------------- SAVE BILL ---------------- #

def save_bill(text):

    with open("restaurant_bills.txt", "a", encoding="utf-8") as file:

        file.write(text)
        file.write("\n")
        file.write("=" * 60)
        file.write("\n")

# ---------------- QR CODE ---------------- #

def show_qr_code(amount):

    upi_id = "yourupiid@oksbi"   # CHANGE THIS

    upi_link = f"upi://pay?pa={upi_id}&pn=Restaurant&am={amount}&cu=INR"

    qr = qrcode.make(upi_link)

    qr = qr.resize((250, 250))

    qr_window = tk.Toplevel(root)
    qr_window.title("QR Payment")
    qr_window.geometry("350x430")
    qr_window.config(bg="white")

    qr_window.lift()
    qr_window.attributes("-topmost", True)

    qr_image = ImageTk.PhotoImage(qr)

    qr_label = tk.Label(
        qr_window,
        image=qr_image,
        bg="white"
    )

    qr_label.image = qr_image
    qr_label.pack(pady=20)

    tk.Label(
        qr_window,
        text=f"Scan To Pay ₹{amount}",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="green"
    ).pack()

    tk.Label(
        qr_window,
        text="Use Google Pay / PhonePe / Paytm",
        font=("Arial", 11),
        bg="white"
    ).pack(pady=10)

# ---------------- GENERATE RECEIPT ---------------- #

def generate_receipt():

    if customer_name.get() == "" or table_number.get() == "":
        messagebox.showerror(
            "Error",
            "Please enter customer details"
        )
        return

    if bill_number.get() == "":
        messagebox.showerror(
            "Error",
            "Please generate bill number first"
        )
        return

    receipt_text.delete(1.0, tk.END)

    date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    receipt_text.insert(tk.END, "================================================\n")
    receipt_text.insert(tk.END, "              RESTAURANT POS BILL\n")
    receipt_text.insert(tk.END, "================================================\n\n")

    receipt_text.insert(tk.END, f"Bill Number : {bill_number.get()}\n")
    receipt_text.insert(tk.END, f"Date & Time : {date_time}\n")
    receipt_text.insert(tk.END, f"Customer    : {customer_name.get()}\n")
    receipt_text.insert(tk.END, f"Table No    : {table_number.get()}\n")

    receipt_text.insert(tk.END, "\n------------------------------------------------\n")
    receipt_text.insert(tk.END, "Items Ordered\n")
    receipt_text.insert(tk.END, "------------------------------------------------\n")

    total = 0

    for item, price in menu_items.items():

        qty = order_quantities[item].get()

        if qty > 0:

            item_total = qty * price

            receipt_text.insert(
                tk.END,
                f"{item} x {qty} = ₹{item_total}\n"
            )

            total += item_total

    if total == 0:
        messagebox.showerror(
            "Error",
            "Please select menu items"
        )
        return

    gst = total * 0.05

    grand_total = total + gst

    receipt_text.insert(tk.END, "\n------------------------------------------------\n")

    receipt_text.insert(tk.END, f"Subtotal        : ₹{total}\n")
    receipt_text.insert(tk.END, f"GST (5%)        : ₹{gst:.2f}\n")
    receipt_text.insert(tk.END, f"Grand Total     : ₹{grand_total:.2f}\n")

    receipt_text.insert(tk.END, "\nPayment Status  : PAID (QR)\n")

    receipt_text.insert(tk.END, "\n================================================\n")
    receipt_text.insert(tk.END, "           THANK YOU - VISIT AGAIN\n")
    receipt_text.insert(tk.END, "================================================\n")

    # Save Bill
    save_bill(receipt_text.get(1.0, tk.END))

    # Show QR
    show_qr_code(round(grand_total, 2))

# ---------------- RESET ---------------- #

def reset_form():

    customer_name.set("")
    table_number.set("")
    bill_number.set("")

    for item in order_quantities:
        order_quantities[item].set(0)

    receipt_text.delete(1.0, tk.END)

# ---------------- TITLE ---------------- #

tk.Label(
    root,
    text="🍽 RESTAURANT POS SYSTEM",
    font=("Helvetica", 24, "bold"),
    bg="#f5f5f5",
    fg="#2c3e50"
).pack(pady=15)

# ---------------- CUSTOMER FRAME ---------------- #

frame1 = tk.Frame(root, bg="white", bd=2, relief="solid")
frame1.pack(pady=10, padx=15, fill="x")

tk.Label(
    frame1,
    text="Customer Details",
    font=("Arial", 15, "bold"),
    bg="white"
).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(
    frame1,
    text="Customer Name:",
    font=("Arial", 11),
    bg="white"
).grid(row=1, column=0, padx=10, pady=5, sticky="w")

tk.Entry(
    frame1,
    textvariable=customer_name,
    width=30
).grid(row=1, column=1, pady=5)

tk.Label(
    frame1,
    text="Table Number:",
    font=("Arial", 11),
    bg="white"
).grid(row=2, column=0, padx=10, pady=5, sticky="w")

tk.Entry(
    frame1,
    textvariable=table_number,
    width=30
).grid(row=2, column=1, pady=5)

tk.Label(
    frame1,
    text="Bill Number:",
    font=("Arial", 11),
    bg="white"
).grid(row=3, column=0, padx=10, pady=5, sticky="w")

tk.Entry(
    frame1,
    textvariable=bill_number,
    width=30,
    state="readonly"
).grid(row=3, column=1, pady=5)

tk.Button(
    frame1,
    text="Generate Bill No",
    bg="#3498db",
    fg="white",
    font=("Arial", 11, "bold"),
    command=generate_bill_no
).grid(row=4, column=0, columnspan=2, pady=12)

# ---------------- MENU FRAME ---------------- #

frame2 = tk.Frame(root, bg="white", bd=2, relief="solid")
frame2.pack(pady=10, padx=15, fill="x")

tk.Label(
    frame2,
    text="🍔 MENU",
    font=("Arial", 16, "bold"),
    bg="white"
).grid(row=0, column=0, columnspan=6, pady=10)

items = list(menu_items.items())

for index, (item, price) in enumerate(items):

    row = index // 2
    col = (index % 2) * 3

    tk.Label(
        frame2,
        text=item,
        font=("Arial", 11),
        bg="white",
        anchor="w",
        width=20
    ).grid(row=row+1, column=col, padx=10, pady=8)

    tk.Label(
        frame2,
        text=f"₹{price}",
        font=("Arial", 11, "bold"),
        fg="green",
        bg="white",
        width=8
    ).grid(row=row+1, column=col+1)

    tk.Spinbox(
        frame2,
        from_=0,
        to=10,
        width=5,
        textvariable=order_quantities[item]
    ).grid(row=row+1, column=col+2, padx=5)

# ---------------- RECEIPT FRAME ---------------- #

frame3 = tk.Frame(root, bg="white", bd=2, relief="solid")
frame3.pack(pady=5, padx=15)

tk.Label(
    frame3,
    text="🧾 BILL RECEIPT",
    font=("Arial", 16, "bold"),
    bg="white"
).pack(pady=8)

receipt_text = tk.Text(
    frame3,
    width=70,
    height=6,
    font=("Courier New", 10)
)

receipt_text.pack(fill="both")

# ---------------- BUTTONS ---------------- #

frame4 = tk.Frame(root, bg="#f5f5f5")
frame4.pack(pady=15)

tk.Button(
    frame4,
    text="Generate Bill",
    bg="#27ae60",
    fg="white",
    font=("Arial", 12, "bold"),
    width=18,
    command=generate_receipt
).grid(row=0, column=0, padx=15)

tk.Button(
    frame4,
    text="Reset",
    bg="#e74c3c",
    fg="white",
    font=("Arial", 12, "bold"),
    width=18,
    command=reset_form
).grid(row=0, column=1, padx=15)

# ---------------- RUN APPLICATION ---------------- #

root.mainloop()