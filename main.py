# Library
import mysql.connector as sql
import tkinter as tk
import tkinter.messagebox

shopping_list = []
products = []
products2 = []


def file(fileName, lst):
    with open(fileName, "r") as f:
        list = f.readlines()
        for ele in list:
            ele.split(",")
            lst.append(ele.replace("\n", ""))


def start(cursor, conn):
    root = tk.Tk()
    root.title("Log in or Register.")
    WIDTH, HEIGHT = 500, 150

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0e387a")
    canvas.pack()

    title = tk.Label(canvas, text="Log In or Register:", font=("Times New Roman", 20), bg="#0e387a")
    title.place(relx=0.3, rely=0.1)

    prev_account = tk.Button(text="Log In", command=lambda: [root.destroy(), login_surface(cursor, conn)], bg="#9fafca")
    prev_account.place(relx=0.1, rely=0.5, relheight=0.2, relwidth=0.3)

    new_account = tk.Button(text="Register", command=lambda: [root.destroy(), register(cursor, conn)], bg="#9fafca")
    new_account.place(relx=0.6, rely=0.5, relheight=0.2, relwidth=0.3)

    root.mainloop()


def login_surface(cursor, conn):
    root = tk.Tk()
    root.title("Log in")
    WIDTH, HEIGHT = 300, 200

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#9fafca")
    canvas.pack()

    title = tk.Label(canvas, text="Log in", font=("Times New Roman", 20), bg="#9fafca")
    title.place(relx=0.35, rely=0.02, relwidth=0.3, relheight=0.25)

    user_title = tk.Label(canvas, text="Username:", font=("Times New Roman", 15), bg="#9fafca")
    user_title.place(relx=0.1, rely=0.3)
    username = tk.Entry(canvas, font=("Times New Roman", 10))
    username.place(relx=0.4, rely=0.32, relwidth=0.5, relheight=0.1)

    pin_title = tk.Label(canvas, text="Pin:", font=("Times New Roman", 15), bg="#9fafca")
    pin_title.place(relx=0.26, rely=0.54)
    pin = tk.Entry(canvas, font=("Times New Roman", 10), show="*")
    pin.place(relx=0.4, rely=0.56, relwidth=0.3, relheight=0.1)

    go = tk.Button(canvas, text="Go", font=("Times New Roman", 15),
                   command=lambda: check_login(cursor, username, pin, conn))
    go.place(relx=0.25, rely=0.75, relwidth=0.5, relheight=0.1)

    root.mainloop()


def check_login(cursor, username, pin, conn):
    cursor.execute("SELECT * FROM accounts WHERE user = %s and pin = %s", (username.get().strip(), pin.get()))
    result = cursor.fetchall()

    if result:
        storegui(cursor, username, conn)
    elif username.get() == "Admin" and pin.get() == "0000":
        admin()
    else:
        tkinter.messagebox.showinfo("Error", "The username or password is incorrect.")


def register(cursor, conn):
    root = tk.Tk()
    WIDTH, HEIGHT = 400, 200
    root.title("Register")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#9fafca")
    canvas.pack()

    title = tk.Label(canvas, text="Register New Account", font=("Times New Roman", 16), bg="#9fafca")
    title.place(relx=0.25, rely=0.02, relwidth=0.5, relheight=0.25)

    user_title = tk.Label(canvas, text="Create an username:", font=("Times New Roman", 12), bg="#9fafca")
    user_title.place(relx=0.15, rely=0.3)
    username = tk.Entry(canvas, font=("Times New Roman", 10))
    username.place(relx=0.47, rely=0.32, relwidth=0.35, relheight=0.1)

    pin_title = tk.Label(canvas, text="Create a pin:", font=("Times New Roman", 12), bg="#9fafca")
    pin_title.place(relx=0.25, rely=0.54)
    pin = tk.Entry(canvas, font=("Times New Roman", 10), show="*")
    pin.place(relx=0.47, rely=0.56, relwidth=0.3, relheight=0.1)

    go = tk.Button(canvas, text="Register!", font=("Times New Roman", 15),
                   command=lambda: [check_register(cursor, username, pin, conn)])
    go.place(relx=0.25, rely=0.75, relwidth=0.5, relheight=0.15)

    root.mainloop()


def check_register(cursor, username, pin, conn):
    cursor.execute("INSERT INTO accounts (user, pin) VALUES (%s, %s)", (username.get(), pin.get()))
    conn.commit()
    tkinter.messagebox.showinfo("Success", "Your account is created. You can now log in!")
    login_surface(cursor, conn)


def storegui(cursor, username, conn):
    root = tk.Tk()
    root.title("Shopping List")
    WIDTH, HEIGHT = 700, 500

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#9fafca")
    canvas.pack()

    title = tk.Label(canvas, text="Add Item", font=("Times New Roman", 20), bg="#9fafca")
    title.place(relx=0.32, relwidth=0.3, relheight=0.1)

    display_products = tk.Listbox(canvas, selectmode='SINGLE', font=("Times New Roman", 17))
    display_products.place(relx=0.02, rely=0.1, relwidth=0.35, relheight=0.87)
    lstbox(display_products, products)

    display_products2 = tk.Listbox(canvas, selectmode='SINGLE', font=("Times New Roman", 17))
    display_products2.place(relx=0.38, rely=0.1, relwidth=0.35, relheight=0.87)
    lstbox(display_products2, products2)

    add_cart = tk.Button(canvas, text="Add the grocery.",
                         command=lambda: [selection(display_products, cursor, username, conn),
                                          selection(display_products2, cursor, username, conn)])
    add_cart.place(relx=0.74, rely=0.2, relheight=0.07, relwidth=0.25)

    view_cart = tk.Button(canvas, text="View Groceries", command=lambda: view_groceries())
    view_cart.place(relx=0.74, rely=0.6, relheight=0.07, relwidth=0.25)

    root.mainloop()


def admin():
    root = tk.Tk()
    root.title("Admin")
    WIDTH, HEIGHT = 350, 250

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#355C7D")
    canvas.pack()

    tk.Label(canvas, text="Admin Settings", bg="#355C7D", font=("Cambria", 25)).place(relx=0.2, rely=0.02)

    newProduct = tk.Entry(canvas, font=("Cambria", 11))
    newProduct.insert(0, "Product to add...")
    newProduct.place(relx=0.32, rely=0.22, relwidth=0.38, relheight=0.1)

    removeProduct = tk.Entry(canvas, font=("Cambria", 11))
    removeProduct.insert(0, "Product to remove...")
    removeProduct.place(relx=0.32, rely=0.37, relwidth=0.38, relheight=0.1)

    searchProduct = tk.Entry(canvas, font=("Cambria", 11))
    searchProduct.insert(0, "Check for product...")
    searchProduct.place(relx=0.32, rely=0.52, relwidth=0.38, relheight=0.1)

    apply_changes = tk.Button(canvas, text="Apply Changes", command=lambda: apply(newProduct.get(), removeProduct.get(),
                                                                                  searchProduct.get()))
    apply_changes.place(relx=0.1, rely=0.8, relwidth=0.3, relheight=0.1)

    log_in = tk.Button(canvas, text="Log In", command=lambda: root.destroy())
    log_in.place(relx=0.6, rely=0.8, relwidth=0.3, relheight=0.1)
    root.mainloop()


def apply(new, removePro, search):
    if not new == "Product to add..." or new.strip() == "":
        if len(products) > len(products2):
            with open('groceryItems.txt', 'a') as f:
                f.write("\n")
                f.write(new)
        else:
            with open('groceryProducts.txt', 'a') as f:
                f.write("\n")
                f.write(new)

    if not removePro == "Product to remove..." or removePro.strip() == "":
        remove("groceryItems.txt", removePro), remove("groceryProducts.txt", removePro)

    if not search == "Check for product..." or search.strip() == "":
        if search in products or search in products2:
            tk.messagebox.showinfo("Success", f"{search} is already in the list of available products.")
        else:
            tk.messagebox.showerror("Not Found", f"{search} was not found in the list of available products.")


def remove(fileName, removeProduct):
    with open(fileName, "r") as f:
        lines = f.readlines()
        with open(fileName, "w") as fi:
            for item in lines:
                if item.strip('\n') != removeProduct:
                    fi.write(item)


def selection(lst, cursor, username, conn):
    curselection = lst.curselection()
    for index in curselection:
        shopping_list.append(lst.get(index))
        cursor.execute('UPDATE accounts SET GroceryList = %s WHERE user = %s', (lst.get(index), username.get()), )
    print(shopping_list)
    conn.commit()


def lstbox(lst, list_items):
    for item in list_items:
        lst.insert("end", item)


def view_groceries():
    root = tk.Tk()
    WIDTH, HEIGHT = 400, 500
    root.title("Register")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#9fafca")
    canvas.pack()

    title = tk.Label(canvas, text="View Groceries", font=("Times New Roman", 16), bg="#9fafca")
    title.place(relx=0.25, rely=0.02, relwidth=0.5)

    display_items = tk.Label(canvas, font=("Times New Roman", 12))
    display_items.place(relx=0.05, rely=0.1, relheight=0.85, relwidth=0.4)
    display_label(display_items)

    delete_product = tk.Entry(canvas)
    delete_product.insert(0, "Enter Item to Delete in Here....")
    delete_product.place(relx=0.5, relwidth=0.4, relheight=0.05, rely=0.45)

    go = tk.Button(canvas, text="Delete", command=lambda: delete(delete_product, display_items))
    go.place(relx=0.57, relwidth=0.25, relheight=0.05, rely=0.51)

    exitGrocery = tk.Button(canvas, text="Exit", command=lambda: exit())
    exitGrocery.place(relx=0.57, relwidth=0.25, relheight=0.05, rely=0.9)
    root.mainloop()


def delete(product, display):
    try:
        shopping_list.remove(product.get())
        display.config(text=" ")
        display_label(display)

    except ValueError:
        tkinter.messagebox.showerror("Error", "That item was not found.")


def display_label(label):
    for item in shopping_list:
        label['text'] += item + "\n"


def main():
    conn = sql.connect(
        host='localhost',
        user='root',
        passwd='vovbUx',
        database='credentials')
    cursor = conn.cursor()

    # cur.execute("CREATE DATABASE credentials")
    # cursor.execute('CREATE TABLE accounts (user VARCHAR(255), pin INTEGER(10))')
    file('groceryProducts.txt', products)
    file('groceryItems.txt', products2)

    start(cursor, conn)


main()
