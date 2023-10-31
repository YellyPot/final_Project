# IMPORTS
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
from tkinter import filedialog
import random
import sqlite3
import random
from datetime import datetime
import time
from datetime import timedelta
import sqlite3

###########
################################################################

window = Tk()
window.maxsize(500, 600)
window.minsize(500, 600)
window.title('SPARduct')

################################################################

tk_font = 'Segoe UI Black'
tk_width = 500
tk_height = 600
bgcolor = "white"
lbcolor = "red"
user_index = 0

######################### LISTS
transaction_list = []
accounts = []
users_LIST = []
products = []
user_info = []
product_list = []
info = []
product_index = 0
products_user_list = {}
ind = 0

cart_list = {}
list_p = []
list_a = []
trans_code = "qwertyuiopasdfghjklzxcvbnm1234567890"

#
date = datetime.now().date()
_time = time.localtime(time.time())


########################## BSU LOGO
################################################################
def open_image():
    global image
    image = Image.open(filedialog.askopenfilename())
    image = image.resize((100, 100))
    image = ImageTk.PhotoImage(image)


############ ACCOUNTS
class Accounts():
    def __init__(self, img, name, age, address, school, username, password):
        self.username = username
        self.password = password
        self.img = img
        self.name = name
        self.address = address
        self.school = school
        self.age = age
        self.prodcut_list = []
        self.product_img = None
        self.product_name = None
        self.product_price = None
        self.product_quan = None
        self.seller_address = None
        self.seller_contact = None
        self.date = datetime.now().date()

    def show_info(self):
        user_frame = LabelFrame(users_frame)
        user_frame.pack(side='left')

        user_image = Label(user_frame, image=self.img)
        user_image.pack()

        user_name = Label(user_frame, text=f"Name : {self.name}")
        user_name.pack()

        user_age = Label(user_frame, text=f"Age : {self.age}")
        user_age.pack()

        user_address = Label(user_frame, text=f"Address : {self.address}")
        user_address.pack()

        user_school = Label(user_frame, text=f"School : {self.school}")
        user_school.pack()

        user_DATE = Label(user_frame, text=f"School : {self.date}")
        user_DATE.pack()

    def get_img(self):
        return self.img

    def get_date(self):
        return self.date

    def get_user_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_user_address(self):
        return self.address

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_school(self):
        return self.school

    def add_product(self, product_img, product_name, product_price, product_quan, seller_address, seller_contact):
        global product_index
        product = Products(product_img, product_name, product_price, product_quan, seller_address, seller_contact)
        self.prodcut_list.append(product)
        product_index += 1

    def show_products(self):
        for items in self.prodcut_list:
            items.show()

    def unshow_my_products(self):
        for items in self.prodcut_list:
            items.unshow()

    def show_cart(self):
        for key in cart_list.keys():
            if key == user_index:
                cart_list.get(key).pack()
            else:
                cart_list.get(key).pack_forget()

    def unshow_cart(self):
        for key in cart_list.keys():
            cart_list.get(key).pack_forget()

    def show_user_products(self):
        for i in range(len(self.prodcut_list)):
            print(i)
            if date == self.prodcut_list[i].time_of_deliver:
                self.prodcut_list.remove(self.prodcut_list[i])
            else:
                self.prodcut_list[i].show_my_product()

    def show_my_transaction(self, name):
        if name == self.name:
            for items in self.prodcut_list:
                for carts in items.transaction_list:
                    carts.pack()
        else:
            pass

    def unshow_my_transaction(self):
        for items in self.prodcut_list:
            for carts in items.transaction_list:
                carts.pack_forget()


class Products(Accounts):
    def __init__(self, product_img, product_name, product_price, product_quan, seller_address, seller_contact):
        global date
        super().__init__(list_a[user_index].get_img(),
                         list_a[user_index].get_user_name(),
                         list_a[user_index].get_age(),
                         list_a[user_index].get_user_address(),
                         list_a[user_index].get_school(),
                         list_a[user_index].get_username(),
                         list_a[user_index].get_password())
        # products components

        self.product_image = product_img
        self.product_name = product_name
        self.product_price = product_price
        self.product_quan = int(product_quan)
        self.seller_address = seller_address
        self.seller_contact = seller_contact
        # time
        self.local_t = time.localtime()
        self.date_posted = datetime.now().date()
        self.time_posted = time.strftime("%H:%M:%S", self.local_t)

        # products frame, labels and buttons
        self.product_container = LabelFrame(product_frame)
        self.product_address_f = Label(self.product_container, text=self.seller_address)
        self.product_contact_f = Label(self.product_container, text=self.seller_contact)
        self.product_quan_f = Label(self.product_container, text=str(self.product_quan))
        self.product_price_f = Label(self.product_container, text=self.product_price)
        self.product_image_f = Label(self.product_container, image=self.product_image)
        self.product_name_f = Label(self.product_container, text=self.product_name)
        self.product_dt_f = Label(self.product_container,
                                  text=f"DATE POSTED: {self.date_posted}\nTIME: {self.time_posted}")
        self.product_container.bind('<Enter>', self.wide_view)
        self.product_container.bind('<Leave>', self.small_view)
        self.view_profile = Button(self.product_container, text='view', command=self.profile_view)
        # buy button
        self.buy_button = Button(self.product_container, text='add to cart')

        # cart frame
        self.cart_f = LabelFrame(cart_frame)

        # transaction frame
        self.transaction_f = Label(user_transaction_frame)
        # trasaction history list
        self.transaction_list = []

        self.frame = Frame(user_frame)
        self.label = Label(self.frame, image=self.img)

        self.button_exit_prof = Button(self.frame, command=self.profile_unview, text="X")

        self.info_label = Label(self.frame,
                                text=f"Name:{self.get_user_name()}\nAge:{self.get_age()}\nAddress:{self.get_user_address()}\nSchool:{self.get_school()}")
        self.label.pack()
        self.info_label.pack()
        self.button_exit_prof.pack()

        # myproducts frame
        self.myproduct_container = LabelFrame(user_products_frame)
        self.myproduct_address_f = Label(self.myproduct_container, text=self.seller_address)
        self.myproduct_contact_f = Label(self.myproduct_container, text=self.seller_contact)
        self.myproduct_quan_f = Label(self.myproduct_container, text=str(self.product_quan))
        self.myproduct_price_f = Label(self.myproduct_container, text=self.product_price)
        self.myproduct_image_f = Label(self.myproduct_container, image=self.product_image)
        self.myproduct_name_f = Label(self.myproduct_container, text=self.product_name)
        self.selfindex = product_index
        self.remove_button = Button(self.myproduct_container, text='remove')

        # date delivever
        self.time_of_deliver = datetime.now().date().today() + timedelta(days=(int(_time.tm_wday) + 5))

    def get_index(self):
        return self.selfindex

    def show(self):
        global product_frame
        product_frame.bind("<Key>", self.move)
        index = user_index

        self.product_image_f.pack()
        self.product_name_f.pack()
        self.product_price_f.pack()
        self.product_quan_f.pack()
        self.product_address_f.pack()
        self.product_contact_f.pack()
        self.product_dt_f.pack()
        self.buy_button.config(command=lambda: self._add_tocart())
        self.product_container.pack()

    def move(self, event):
        self.product_container.place(x=200, y=self.product_container.winfo_y() + 10)
        window.update()

    def unshow(self):
        self.product_dt_f.pack_forget()
        self.myproduct_image_f.pack_forget()
        self.myproduct_name_f.pack_forget()
        self.myproduct_price_f.pack_forget()
        self.myproduct_quan_f.pack_forget()
        self.myproduct_address_f.pack_forget()
        self.myproduct_contact_f.pack_forget()
        self.myproduct_container.pack_forget()
        self.remove_button.pack_forget()

    def unpack(self):
        self.product_container.pack_forget()
        self.myproduct_container.pack_forget()

    def show_my_product(self):
        self.myproduct_image_f.pack()
        self.myproduct_name_f.pack()
        self.myproduct_price_f.pack()
        self.myproduct_quan_f.pack()
        self.myproduct_address_f.pack()
        self.myproduct_contact_f.pack()
        self.myproduct_container.pack()
        self.remove_button.pack()

    def wide_view(self, event):

        self.buy_button.pack()
        self.view_profile.pack()

    def small_view(self, event):
        self.buy_button.pack_forget()
        self.view_profile.pack_forget()

    def _add_tocart(self):

        global list_p
        global user_index
        product_frame.pack_forget()
        cart_frame.pack_forget()
        product_frame.pack_forget()
        menu_frame.pack_forget()

        buy_frame.pack()

        product_picture.config(image=self.product_image)

        amount.config(text=str('PHP' + str(self.product_price)))

        new_quan = StringVar()
        quan_menu.config(textvariable=new_quan, from_=0, to=self.product_quan)

        buy_button.config(command=lambda: self.tran(new_quan.get()), text="BUY")

    def tran(self, new_quan):
        ask = messagebox.askyesno("info", "are you sure to buy this product?")
        if ask:
            global trans_code
            code = ''
            quan = self.product_quan

            for i in range(5):
                code += str(trans_code[random.randint(0, 35)])
            self.product_quan -= int(new_quan)
            self.product_quan_f.config(text=str(self.product_quan))
            self.myproduct_quan_f.config(text=(str(self.product_quan)))

            print(self.product_quan)
            window.update()
            if self.product_quan <= 0:
                self.product_quan_f.config(text='sold out')
                self.buy_button.config(state=DISABLED)

            # save to the cart
            price = int(self.product_price)
            payment = str(int(new_quan) * price)
            product_p_c = Label(self.cart_f, image=self.product_image)
            product_info_c = Label(self.cart_f,
                                   text=f"Seller: {self.get_user_name()}\nProduct: {self.product_name}\nAmount: {self.product_price}\nQuantity: {quan}\nTransaction Code: {str(code)}\nPayment: {payment}\nDATE: {date}\nDATE OF DELIVER:{self.time_of_deliver}")

            product_p_c.pack()
            product_info_c.pack()
            cart_list.update({user_index: self.cart_f})

            # save the transaction
            product_p_t = Label(self.transaction_f, image=self.product_image)
            product_info_t = Label(self.transaction_f,
                                   text=f"Buyer: {list_a[user_index].get_user_name()}\nBuyer address:{list_a[user_index].get_user_address()}Product: {self.product_name}\nAmount: {self.product_price}\nQuantity: {quan}\nTransaction Code: {str(code)}\nPayment: {payment}\nDATE OF DELIVER:{self.time_of_deliver}")
            product_p_t.pack()
            product_info_t.pack()
            self.transaction_list.append(self.transaction_f)

            # send transaction to the admin
            transaction_list.append(
                str(f"Product:{self.product_name} | Seller:{self.get_user_name()} | Price:{self.product_price} >> Buyer:{list_a[user_index].get_user_name()} | Payment:{payment} | TRANSACTION CODE:{code}"))
        else:
            pass

    def profile_view(self):
        product_frame.pack_forget()
        sell_frame.pack_forget()
        cart_frame.pack_forget()
        profile_frame.pack_forget()
        menu_frame.pack_forget()

        self.frame.pack(expand=True, fill=BOTH)

    def profile_unview(self):
        self.frame.pack_forget()
        product_frame.pack(expand=True, fill=BOTH)

    def payment_frame(self):
        pass

    def get_name(self):
        return self.product_name

    def get_pro_date(self):
        return f"{self.date_posted}| {self.time_posted}"

    def get_image(self):
        return self.product_image

    def get_price(self):
        return self.product_price

    def remove_product(self):
        self.product_container.destroy()

    def get_address(self):
        return self.seller_address

    def get_contact(self):
        return self.seller_contact

    def get_quan(self):
        return self.product_quan


################################################################

def save_product(product_image, product_name, product_price, product_quan, seller_address, seller_contact):
    global product_index
    global product_frame

    x = log_in_username.get() + ' ' + log_in_password.get()
    if not (
            product_image == None and product_name == "" and product_price == '' and product_quan == '' and seller_address == '' and seller_contact == ''):

        product = Products(product_image, product_name, product_price, product_quan, seller_address, seller_contact)
        list_a[user_index].add_product(product_image,
                                       product_name,
                                       product_price,
                                       product_quan,
                                       seller_address,
                                       seller_contact)
        list_p.append(product)

        info_save = {x: product}
        products.append(info_save)

        product.show()

    else:
        return messagebox.showerror('error', 'error')


def product_validation():
    save_product(product_image, upload_name_of_product.get(),
                 upload_price.get(),
                 upload_stock.get(),
                 upload_address.get(),
                 upload_contact.get())


def upload_image_function():
    global product_image
    product_image = Image.open(filedialog.askopenfilename())
    product_image = product_image.resize((50, 50))
    product_image = ImageTk.PhotoImage(product_image)


#######################  SAVE ACCOUNT

def save_account(image, name, age, address, school, username, password):
    account = Accounts(image, name, age, address, school, username, password)
    list_a.append(account)


#######################  ADMIN

def admin():
    log_in_canvas.pack_forget()
    admin_frame.pack(expand=True, fill=BOTH)

    # for display users
    for acc in list_a:
        acc.show_info()

    for items in range(len(transaction_list)):
        label = Label(admin_tran_frame, text=str(transaction_list[items]))
        label.pack()
    for pro in list_p:
        label2 = Label(inven_frame, image=pro.get_image())
        label2.pack()
        info_p = Label(inven_frame,
                       text=f"product:{pro.get_name()}\nprice:{pro.get_price()}\nStock:{pro.get_quan()}\nAddress:{pro.get_address()}\nContact:{pro.get_contact()}\nDATE POSTED:{pro.get_pro_date()}")
        info_p.pack()


def users(event):
    admin_menu_frame.pack_forget()
    inven_frame.pack_forget()
    admin_tran_frame.pack_forget()

    users_frame.pack(expand=True, fill=BOTH)


def inventory(event):
    admin_menu_frame.pack_forget()
    users_frame.pack_forget()
    admin_tran_frame.pack_forget()

    inven_frame.pack(expand=True, fill=BOTH)


def admin_log_out():
    pass


def admin_menu(event):
    users_frame.pack_forget()
    inven_frame.pack_forget()
    admin_tran_frame.pack_forget()

    admin_menu_frame.pack(expand=True, fill=BOTH)


def admin_tran(event):
    users_frame.pack_forget()
    inven_frame.pack_forget()
    admin_menu_frame.pack_forget()

    admin_tran_frame.pack(expand=True, fill=BOTH)


#######################   USERS


def user():
    window.update()


def home():
    log_in_canvas.pack_forget()
    user_frame.pack(fill=BOTH, expand=True)
    for items in range(len(list_a)):
        for x in list_a[items].prodcut_list:
            x.product_container.pack()

    # display user data such as cart,products and transaction hirtory
    for items in range(len(list_a)):
        if items == user_index:
            list_a[items].show_cart()
            list_a[items].show_user_products()
            list_a[items].show_my_transaction(list_a[user_index].get_user_name())
        else:
            list_a[items].unshow_cart()
            list_a[items].unshow_my_products()
            list_a[items].unshow_my_transaction()


def show_products(event):
    global products
    sell_frame.pack_forget()
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    for x in list_a[user_index].prodcut_list:
        x.product_container.pack()

    product_frame.pack(expand=True, fill=BOTH)


def myproducts(event):
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_transaction_frame.pack_forget()
    sell_frame.pack_forget()

    for items in range(len(list_a)):
        if items == user_index:
            list_a[items].show_user_products()
        else:
            list_a[items].unshow_my_products()

    user_products_frame.pack(expand=True, fill=BOTH)


def mytransaction(event):
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    sell_frame.pack_forget()

    user_transaction_frame.pack(expand=True, fill=BOTH)


def add_product(event):
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    sell_frame.pack(expand=True, fill=BOTH)


def remove_product():
    pass


def menu(event):
    user_products_frame.pack_forget()
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    sell_frame.pack_forget()
    buy_frame.pack_forget()
    user_transaction_frame.pack_forget()

    menu_frame.pack(expand=True, fill=BOTH)


def cart(event):
    sell_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    for key in cart_list.keys():
        if key == user_index:
            cart_list.get(key).pack()
        else:
            cart_list.get(key).pack_forget()
    cart_frame.pack(expand=True, fill=BOTH)


def profile(event):
    menu_frame.pack_forget()
    sell_frame.pack_forget()
    cart_frame.pack_forget()
    product_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    global user_index
    profile_frame.pack(expand=True, fill=BOTH)

    profile_pic.config(image=list_a[user_index].get_img())
    profile_NAME.config(text=list_a[user_index].get_user_name())
    profile_ADDRES.config(text=list_a[user_index].get_user_address())
    profile_AGE.config(text=list_a[user_index].get_age())
    profile_SCHOOL.config(text=list_a[user_index].get_school())
    profile_DATE.config(text=list_a[user_index].get_date())


# x = susername.get() + "=" + s_password.get()

#   print(info[0].get(x)['x'])

def user_log_out(event):
    cart_frame.pack_forget()
    user_frame.pack_forget()
    welcome()


def about():
    pass

################################################################
# center the window
def center_window(window, width, height, ):
    screen_width = window.winfo_screenwidth()
    screen_heigth = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_heigth - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

################################################################

def welcome():
    home_canvas.pack(expand=True, fill=BOTH)

###############################################################

def sign_in_validation():
    global image
    if not (
            image == None or sign_user_name.get() == '' or age.get() == sign_user_address.get() == '' or sign_user_school.get() == ''):
        ##### SAVE ACCOUNT
        if s_password.get() == confirm_pass.get():
            save_account(image,
                         sign_user_name.get(),
                         age.get(),
                         sign_user_address.get(),
                         sign_user_school.get(),
                         susername.get(),
                         s_password.get())
            show_log_in_frame()
    else:
        show_sign_in_frame()


################################################################

def log_in_validation():
    global user_index
    if log_in_username.get() == "admin" and log_in_password.get() == 'admin':
        admin()
    else:
        x = log_in_username.get() + "=" + log_in_password.get()

        for i in range(len(list_a)):
            if log_in_username.get() == list_a[i].get_username() and log_in_password.get() == list_a[i].get_password():
                user_index = i
                home()

################################################################
def show_log_in_frame():
    sign_in_canvas.pack_forget()

    home_canvas.pack_forget()

    log_in_canvas.pack(expand=True, fill=BOTH)


################################################################

def show_sign_in_frame():
    log_in_canvas.pack_forget()
    sign_in_canvas.pack(expand=True, fill=BOTH)


################################################################
############ center the window
center_window(window, tk_width, tk_height)
########################## BSU LOGO

logo_big = Image.open('images/logo.png')
logo_big = logo_big.resize((100, 100))
logo_big = ImageTk.PhotoImage(logo_big)

logo_med = Image.open('images/logo.png')
logo_med = logo_med.resize((80, 80))
logo_med = ImageTk.PhotoImage(logo_med)

logo_small = Image.open('images/logo.png')
logo_small = logo_small.resize((50, 50))
logo_small = ImageTk.PhotoImage(logo_small)

user_logo = Image.open('images/user.png')
user_logo = user_logo.resize((20, 20))
user_logo = ImageTk.PhotoImage(user_logo)

search_logo = Image.open('images/search logo.png')
search_logo = search_logo.resize((20, 20))
search_logo = ImageTk.PhotoImage(search_logo)

menu_logo = Image.open('images/menu-burger.png')
menu_logo = menu_logo.resize((25, 20))
menu_logo = ImageTk.PhotoImage(menu_logo)

product_logo = Image.open('images/shopping-cart (1).png')
product_logo = product_logo.resize((20, 20))
product_logo = ImageTk.PhotoImage(product_logo)

bg_img = Image.open('images/homebg.jpg')
bg_img = bg_img.resize((tk_width, 700))
bg_img = ImageTk.PhotoImage(bg_img)

bg_2 = Image.open('images/bg2.png')
bg_2 = bg_2.resize((tk_width, 700))
bg_2 = ImageTk.PhotoImage(bg_2)

########################## ADMIN WINDOW

admin_frame = Frame(window)
############

admin_label = Label(admin_frame, text="Admin", font=(tk_font, 10), bg=bgcolor)
admin_label.pack(fill=BOTH)

############

admin_frames_but = LabelFrame(admin_frame,
                              bg=bgcolor,
                              highlightcolor='black',
                              highlightthickness=1,
                              highlightbackground='black'
                              )
admin_frames_but.pack(fill=X)

#
inventory_frame_but = Label(admin_frames_but,
                            text='Inventory',
                            width=15
                            )
inventory_frame_but.pack(side='left')
inventory_frame_but.bind('<Button>', inventory)

#
users_frame_but = Label(admin_frames_but,
                        text='Users',
                        width=15
                        )
users_frame_but.pack(side='left')
users_frame_but.bind('<Button>', users)
#
admin_tran_frame_but = Label(admin_frames_but,
                             text='Transaction',
                             width=15
                             )
admin_tran_frame_but.pack(side='left')
admin_tran_frame_but.bind('<Button>', admin_tran)

#
admin_menu_frame_but = Label(admin_frames_but,
                             text='Menu',
                             width=23
                             )
admin_menu_frame_but.pack(side='right')
admin_menu_frame_but.bind('<Button>', admin_menu)

########################## INVENTORY WINDOW FRAME

inven_frame = Frame(admin_frame, bg='red')

########################## USERS WINDOW FRAME

users_frame = Frame(admin_frame, bg='blue')

########################## ADMIN MENU WINDOW FRAME

admin_menu_frame = Frame(admin_frame, bg='green')

########################### ADMIN TRANSACTION WINDOW FRAME

admin_tran_frame = Frame(admin_frame, bg='black')
########################## USER WINDOW FRAME


user_frame = Frame(window, bg=bgcolor)

##########
header = Label(user_frame, bg='red')
header.pack(fill=X, side=TOP)

top_logo = Label(header, image=logo_small, bg='red')
top_logo.pack(side='left')

title_text = Label(header, text="SARduct",
                   bg=lbcolor,
                   font=('ink free', 12, "bold")
                   )
title_text.pack(side='left')

search_button = Button(header,
                       text="search",
                       bg='white',
                       highlightthickness=0,
                       image=search_logo
                       # command=lambda: search_product_type(search.get())
                       )

search_button.pack(side="right")
search = Entry(header,
               bg="white")

search.pack(side="right")

############

user_frames_but = LabelFrame(user_frame,
                             bg=bgcolor,
                             highlightcolor='black',
                             highlightthickness=1,
                             highlightbackground='black'
                             )
user_frames_but.pack(fill=X)

#
product_frame_but = Label(user_frames_but,
                          image=product_logo,
                          width=30
                          )
product_frame_but.pack(side='left')
product_frame_but.bind('<Button>', show_products)

add_frame_but = Label(user_frames_but,
                      text='Upload',
                      width=10
                      )

add_frame_but.pack(side='left')
add_frame_but.bind('<Button>', add_product)

#
cart_frame_but = Label(user_frames_but,
                       text='Cart',
                       width=10
                       )

cart_frame_but.pack(side='left')
cart_frame_but.bind('<Button>', cart)
#
myproducts_but = Label(user_frames_but,
                       text='Myproducts',
                       width=10
                       )

myproducts_but.pack(side='left')
myproducts_but.bind('<Button>', myproducts)
#
user_transact_but = Label(user_frames_but,
                          text='transaction',
                          width=10
                          )

user_transact_but.pack(side='left')
user_transact_but.bind('<Button>', mytransaction)
#
profile_frame_but = Label(user_frames_but,
                          width=30,
                          image=user_logo
                          )
profile_frame_but.pack(side='left')
profile_frame_but.bind('<Button>', profile)

#
menu_fame_but = Label(user_frames_but,
                      image=menu_logo,
                      width=30
                      )
menu_fame_but.pack(side="right")
menu_fame_but.bind('<Button>', menu)

########################## buy frame

buy_frame = Frame(user_frame)
label = Label(buy_frame, text='BUY')
label.pack(side=TOP)

product_picture = Label(buy_frame)
product_picture.pack(side=TOP)

amount = Label(buy_frame)
amount.pack(side=LEFT)

new_quan = StringVar()
quan_menu = Spinbox(buy_frame)
quan_menu.pack(side=RIGHT)

buy_button = Button(buy_frame)
buy_button.pack(side=BOTTOM)

########################## MENU WINDOW FRAME

menu_frame = Frame(user_frame, bg='black')
bg_menu = Label(menu_frame, image=bg_img)
bg_menu.pack(expand=True, fill=BOTH)

menu = Frame(bg_menu, width=200)
menu.pack(side='right', fill=Y)

log_out = Label(menu, text="Log out")
log_out.pack()
log_out.bind('<Button>', user_log_out)

########################## ADD PRODUCT WINDOW FRAME

sell_frame = Frame(user_frame, bg='yellow')

product_image = None
upload_image = Button(sell_frame, command=lambda: upload_image_function())
upload_image.pack()

upload_name_of_product = Entry(sell_frame)
upload_name_of_product.pack()

upload_price = Entry(sell_frame)
upload_price.pack()

upload_stock = Entry(sell_frame)
upload_stock.pack()

upload_address = Entry(sell_frame)
upload_address.pack()

upload_contact = Entry(sell_frame)
upload_contact.pack()

upload_product = Button(sell_frame, command=product_validation)
upload_product.pack()
########################## CART WINDOW FRAME

cart_frame = Frame(user_frame, bg='red')

########################## PROFILE WINDOW FRAME

profile_frame = Frame(user_frame,
                      bg=bgcolor,

                      )
bg_prof = Label(profile_frame, image=bg_2)
bg_prof.pack()

profile_outine = Frame(bg_prof,
                       highlightcolor='black',
                       highlightthickness=1,
                       highlightbackground='black',
                       pady=50,
                       padx=100,
                       bg=bgcolor
                       )
profile_outine.place(x=60, y=20)
profile_pic = Label(profile_outine,
                    highlightcolor='black',
                    highlightthickness=1,
                    highlightbackground='black',
                    borderwidth=2
                    )
profile_pic.pack()

seperator = Label(profile_outine, text="______________________________", bg=bgcolor)
seperator.pack()

profile_name_L = Label(profile_outine,
                       text='NAME',
                       font=(tk_font, 8, 'bold'),
                       bg=bgcolor)
profile_NAME = Label(profile_outine,
                     bg=bgcolor,
                     font=(tk_font, 18, 'bold')
                     )
profile_name_L.pack()
profile_NAME.pack()

profile_age_L = Label(profile_outine,
                      text='AGE',
                      font=(tk_font, 8, 'bold'),
                      bg=bgcolor)
profile_AGE = Label(profile_outine,
                    bg=bgcolor,
                    font=(tk_font, 18, 'bold')
                    )
profile_age_L.pack()
profile_AGE.pack()

profile_address_L = Label(profile_outine,
                          text='ADDRESS',
                          font=(tk_font, 8, 'bold'),
                          bg=bgcolor)
profile_ADDRES = Label(profile_outine,
                       bg=bgcolor,
                       font=(tk_font, 18, 'bold')
                       )
profile_address_L.pack()
profile_ADDRES.pack()

profile_school_L = Label(profile_outine,
                         text='SCHOOL',
                         font=(tk_font, 8, 'bold'),
                         bg=bgcolor)
profile_SCHOOL = Label(profile_outine,
                       bg=bgcolor,
                       font=(tk_font, 18, 'bold')
                       )
profile_school_L.pack()
profile_SCHOOL.pack()

profile_DATE_l = Label(profile_outine,
                       text='MEMBERSHIP DATE',
                       font=(tk_font, 8, 'bold'),
                       bg=bgcolor)
profile_DATE = Label(profile_outine,
                     bg=bgcolor,
                     font=(tk_font, 18, 'bold')
                     )
profile_DATE_l.pack()
profile_DATE.pack()

########################## PRODUCTS WINDOW FRAME

product_frame = Frame(user_frame, bg='green')

########################## USER PRODUCTS WINDOW FRAME

user_products_frame = Frame(user_frame, bg='orange')
########################## USER transaction WINDOW FRAME

user_transaction_frame = Frame(user_frame, bg='brown')

########################## SIGN UP WINDOW FRAME

sign_in_canvas = Canvas(window)
#########

sign_in_canvas.create_image(250, 250, image=bg_img)

########
outline = LabelFrame(sign_in_canvas, bg=bgcolor, padx=100, pady=18)
outline.place(x=35, y=30)

#############

# logo
sign_logo = Label(outline, image=logo_med, bg=bgcolor)
sign_logo.pack()

# sign label
sign_label = Label(outline,
                   bg=bgcolor,
                   text='Sign in',
                   font=(tk_font, 18, 'bold'),
                   height=2)
sign_label.pack()

# insert user profile

image = None
insert_profile = Button(outline, text="Upload photo",
                        bg='red',
                        font=(tk_font, 8),
                        command=lambda: open_image())
insert_profile.pack(anchor=W)

# sign user full name
sign_user_name_label = Label(outline,
                             text="Name",
                             font=(tk_font, 8),
                             height=1)
sign_user_name_label.pack(anchor=W)
sign_user_name = Entry(outline, font=(tk_font, 8))
sign_user_name.pack(anchor=W)

# sign user school
sign_user_school_label = Label(outline,
                               text="School",
                               font=(tk_font, 8),
                               height=1)
sign_user_school_label.pack(anchor=W)
sign_user_school = Entry(outline, font=(tk_font, 8))
sign_user_school.pack(anchor=W)

# sign address
sign_user_address_label = Label(outline,
                                text="Address",
                                font=(tk_font, 8),
                                height=1)
sign_user_address_label.pack(anchor=W)
sign_user_address = Entry(outline, font=(tk_font, 8), width=30)
sign_user_address.pack(anchor=W)

# sign user age
age_label = Label(outline,
                  bg=bgcolor,
                  text="AGE",
                  font=(tk_font, 8),
                  height=1
                  )

age_label.pack(anchor=W
               )
age = Entry(outline,
            highlightthickness=2,
            highlightcolor='black',
            width=30,
            font=(tk_font, 9)
            )
age.pack(anchor=W)

# sign user name
suser_name_label = Label(outline,
                         text="USERNAME",
                         bg=bgcolor,
                         font=(tk_font, 8),
                         height=1
                         )
suser_name_label.pack(anchor=W)

# sign user username entry
susername = Entry(outline,
                  highlightthickness=2,
                  highlightcolor='black',
                  width=30,
                  font=(tk_font, 8))
susername.pack(anchor=W)

# sign user password
spass_label = Label(outline,
                    text="PASSWORD",
                    bg=bgcolor,
                    font=(tk_font, 8),
                    height=1)

spass_label.pack(anchor=W)

# sign user password entry
s_password = Entry(outline,
                   highlightthickness=2,
                   highlightcolor='black',
                   width=30,
                   font=(tk_font, 8),
                   show="*")
s_password.pack(anchor=W)

# confirm pass word label / input
confirm_pass_label = Label(outline,
                           text="CONFIRM PASSWORD",
                           bg=bgcolor,
                           font=(tk_font, 8),
                           height=1
                           )
confirm_pass_label.pack(anchor=W)

# sign confirm password entry
confirm_pass = Entry(outline,
                     highlightthickness=2,
                     highlightcolor='black',
                     width=30,
                     font=(tk_font, 8),
                     show="*")
confirm_pass.pack(anchor=W)

# sign in button
sign_buttton = Button(outline,
                      text='Sign in',
                      bg=lbcolor,
                      command=sign_in_validation,
                      font=(tk_font, 10),
                      width=10)
sign_buttton.pack()

########################## LOG IN  PRODUCT WINDOW FRAME


log_in_canvas = Canvas(window)
#########

log_in_b = Image.open('images/log in.png')
log_in_b = log_in_b.resize((60, 20))
log_in_b = ImageTk.PhotoImage(log_in_b)

sign_in_b = Image.open('images/signin.png')
sign_in_b = sign_in_b.resize((60, 20))
sign_in_b = ImageTk.PhotoImage(sign_in_b)

######## background
log_in_canvas.create_image(250, 250, image=bg_img)
###########
log_in_outline = Frame(log_in_canvas,
                       bg=bgcolor,
                       highlightcolor='black',
                       highlightthickness=1,
                       highlightbackground='black',
                       padx=100,
                       pady=18
                       )

log_in_outline.place(x=60, y=60)
############
log_in_logo = Label(log_in_outline,
                    image=logo_med,
                    bg=bgcolor
                    )
log_in_logo.pack()
###########
log_in = Label(log_in_outline,
               text='Log in',
               foreground='black',
               font=(tk_font, 23),
               bg=bgcolor
               )
log_in.pack()
###########
space1 = Label(log_in_outline, bg=bgcolor)
space1.pack()
#########
log_in_username_label = Label(log_in_outline,
                              text='Username',
                              foreground='black',
                              font=(tk_font, 13),
                              bg=bgcolor
                              )
log_in_username_label.pack()
log_in_username = Entry(log_in_outline,
                        highlightthickness=2,
                        highlightcolor='black',
                        width=25,
                        show="*",
                        font=(tk_font, 9))
log_in_username.pack()
#########

log_in_password_label = Label(log_in_outline,
                              text='Password',
                              foreground='black',
                              font=(tk_font, 13),
                              bg=bgcolor
                              )
log_in_password_label.pack()
log_in_password = Entry(log_in_outline,
                        highlightthickness=2,
                        highlightcolor='black',
                        width=25,
                        font=(tk_font, 9))
log_in_password.pack()

##########
error = Label(log_in_outline, bg=bgcolor, height=2)
error.pack()
##########
log_in_button = Button(log_in_outline,
                       command=log_in_validation,
                       text='Log in',
                       foreground='white',
                       font=('monosacpe', 10, 'bold'),
                       bg='red',
                       highlightbackground='black',
                       highlightthickness=2,
                       highlightcolor='black')
log_in_button.pack()
#########
space = Label(log_in_outline, bg=bgcolor)
space.pack()
##########
log_in_create_acc_button = Button(log_in_outline,
                                  command=show_sign_in_frame,
                                  text='Sign in',
                                  foreground='white',
                                  font=('monosacpe', 10, 'bold'),
                                  bg='red',
                                  highlightbackground='black',
                                  highlightthickness=2,
                                  highlightcolor='black'
                                  )
log_in_create_acc_button.pack()
#########
space2 = Label(log_in_outline, bg=bgcolor, height=2)
space2.pack()
########################## WELCOCME HOME WINDOW FRAME
con = Image.open('images/icons8-log-in-50.png')
con = ImageTk.PhotoImage(con)

logo_spar = Image.open('images/logo_spar.png')
logo_spar = logo_spar.resize((340, 380))
logo_spar = ImageTk.PhotoImage(logo_spar)
#########

home_canvas = Canvas(window, bg=bgcolor)

home_canvas.create_image(250, 250, image=bg_2)

home_canvas.create_image(30, 30,
                         image=logo_small)
home_canvas.create_image(230, 120, image=logo_spar)
#########
home_con_button = Button(home_canvas,
                         image=con,
                         font=(tk_font, 13, "bold"),
                         bg='red',
                         command=show_log_in_frame, relief=GROOVE)
home_con_button.place(x=220, y=515)

################################################################

if __name__ == '__main__':
    welcome()

window.mainloop()
