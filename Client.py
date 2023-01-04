import socket
import threading
import tkinter as tk
import time
from tkinter import messagebox as msg

current_balance = 1000

HOST = '127.0.0.1' # CHANGE THIS IP ACCORDING TO YOUR CLIENT ADDRESSES
PORT = 9999

VALUE = 0 #For testing in terminal the current balance can be removed

def listen_for_message_from_server():
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]
            value = VALUE #For testing in terminal the current balance can be removed
            print("value is ", value)#For testing in terminal the current balance can be removed
            value = int(content)
            print("value is ", value) #For testing in terminal the current balance can be removed
            print(f"[{username}] {content}")
            global current_balance
            current_balance = value
            print(current_balance) #For testing in terminal the current balance can be removed
            app.shared_data['Balance'].set(current_balance)


        else:
            print(f"The message send from client is empty")

def send_message_to_server(bal):
    while 1:
        message = str(bal)
        if message != '':
            client.sendall(message.encode('utf-8'))
            print("sending....")
        else:
            print("Empty message")
            exit(0)
        return

def communicate_to_server():
    username = "PC2" # Name of clients to log in server
    if username != '':
        client.sendall(username.encode())
    else:
        print("username cant be empty")
        exit(0)


# threading.Thread(target=listen_for_message_from_server, args=()).start()

# send_message_to_server(client)


def nmain():
    # Creating a socket object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    global client
    client = (socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    # add_message("[SERVER] Successfully connected to the server")
    except:
        print(f"Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    communicate_to_server()
    return

def check_for_change():
    if(listen_for_message_from_server()):
        current_balance = listen_for_message_from_server()

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance': tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, WithdrawPage, DepositPage, BalancePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669900')
        self.controller = controller

        self.controller.title('Test Bank')
        self.controller.state('zoomed')
        self.controller.iconphoto(False,tk.PhotoImage(file='atm.png'))

        heading_label = tk.Label(self,
                                 text='Test Bank',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#669900')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#669900')
        space_label.pack()

        password_label = tk.Label(self,
                                  text='Enter your PIN:',
                                  font=('orbitron', 16, 'bold'),
                                  bg='#669900',
                                  fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,
                                      textvariable=my_password,
                                      font=('orbitron', 12),
                                      width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')

        password_entry_box.bind('<FocusIn>', handle_focus_in)

        def check_password():
            print("its clicked")
            if my_password.get() == '123':
                my_password.set('')
                incorrect_password_label['text'] = ''
                controller.show_frame('MenuPage')
            else:
                incorrect_password_label['text'] = 'Incorrect Password'
        def checkkk(_):
            print("zehahah")
            if my_password.get() == '123':
                my_password.set('')
                incorrect_password_label['text'] = ''
                controller.show_frame('MenuPage')
            else:
                incorrect_password_label['text'] = 'Incorrect Password'
        #password_entry_box.bind('<Return>', check_password)

        enter_button = tk.Button(self,
                                 text='Enter',
                                 command=check_password,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)
        password_entry_box.bind('<Return>', checkkk)

        incorrect_password_label = tk.Label(self,
                                            text='',
                                            font=('orbitron', 13),
                                            fg='white',
                                            bg='#33334d',
                                            anchor='n')
        incorrect_password_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()   

class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669900')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Test Bank',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#669900')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self,
                                   text='WELCOME!',
                                   font=('orbitron', 18, 'bold'),
                                   fg='white',
                                   bg='#669900')
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                   text='Please make a selection',
                                   font=('orbitron', 16, 'bold', 'italic'),
                                   fg='white',
                                   bg='#669900',
                                   anchor='w')
        #selection_label.config(anchor='center')
        selection_label.pack()

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def withdraw():
            controller.show_frame('WithdrawPage')

        withdraw_button = tk.Button(button_frame,
                                    text='Withdraw',
                                    font=('orbitron', 14),
                                    command=withdraw,
                                    relief='raised',
                                    borderwidth=3,
                                    width=30,
                                    height=3)
        withdraw_button.pack(side = 'left', expand = True,pady=5)

        def deposit():
            controller.show_frame('DepositPage')

        deposit_button = tk.Button(button_frame,
                                   text='Deposit',
                                   font=('orbitron', 14),
                                   command=deposit,
                                   relief='raised',
                                   borderwidth=3,
                                   width=30,
                                   height=3)
        deposit_button.pack(side = 'left', expand = True,pady=5)

        def balance():
            controller.show_frame('BalancePage')

        balance_button = tk.Button(button_frame,
                                   text='Balance',
                                   font=('orbitron', 14),
                                   command=balance,
                                   relief='raised',
                                   borderwidth=3,
                                   width=30,
                                   height=3)
        balance_button.pack(side = 'left', expand = True,pady=5)

        def exit():
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                text='Exit',
                                font=('orbitron', 14, 'bold'),
                                command=exit,
                                fg='white', bg='orange',
                                relief='raised',
                                borderwidth=3,
                                width=20,
                                height=3)
        exit_button.pack(pady=5, expand = True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()

class WithdrawPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669900')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Test Bank',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#669900')
        heading_label.pack(pady=25)

        choose_amount_label = tk.Label(self,
                                       text='Choose the amount you want to withdraw',
                                       font=('orbitron', 16),
                                       fg='white',
                                       bg='#669900')
        choose_amount_label.pack()

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def notes_dispence(amount):
            money=amount
            notes=[5000,2000,500,200,100,50,20,10,5,2,1]
            count={}
            for i in notes:
                x=money//i
                count[i]=x
                money=money-i*x
            print("\nSent dispense command to counting machine:")

        def check_for_possible_withdraw(current_balance,amount):
            if amount>current_balance:
                msg.showerror("Attention!!", "Insufficent Balance\n")
                exit()
                return False
            else:
                exit()
                return True
            

        def withdraw(amount):
            global current_balance
            hello=check_for_possible_withdraw(current_balance,amount)
            if hello:
                current_balance -= amount
                notes_dispence(amount)
                try:
                    send_message_to_server(current_balance)
                except:
                    print("withdraw over network unsuccessful")
                print("check")
                controller.shared_data['Balance'].set(current_balance)
                controller.show_frame('MenuPage')
                msg.showinfo("Information", "Please Collecr Your Cash!")

        twenty_button = tk.Button(button_frame,
                                  text='20',
                                  command=lambda: withdraw(20),
                                  relief='raised',
                                  borderwidth=3,
                                  width=50,
                                  height=4)
        twenty_button.grid(row=0, column=0, pady=5)

        forty_button = tk.Button(button_frame,
                                 text='40',
                                 command=lambda: withdraw(40),
                                 relief='raised',
                                 borderwidth=3,
                                 width=50,
                                 height=4)
        forty_button.grid(row=1, column=0, pady=5)

        sixty_button = tk.Button(button_frame,
                                 text='60',
                                 command=lambda: withdraw(60),
                                 relief='raised',
                                 borderwidth=3,
                                 width=50,
                                 height=4)
        sixty_button.grid(row=2, column=0, pady=5)

        eighty_button = tk.Button(button_frame,
                                  text='80',
                                  command=lambda: withdraw(80),
                                  relief='raised',
                                  borderwidth=3,
                                  width=50,
                                  height=4)
        eighty_button.grid(row=3, column=0, pady=5)

        one_hundred_button = tk.Button(button_frame,
                                       text='100',
                                       command=lambda: withdraw(100),
                                       relief='raised',
                                       borderwidth=3,
                                       width=50,
                                       height=4)
        one_hundred_button.grid(row=0, column=1, pady=5, padx=555)

        two_hundred_button = tk.Button(button_frame,
                                       text='200',
                                       command=lambda: withdraw(200),
                                       relief='raised',
                                       borderwidth=3,
                                       width=50,
                                       height=4)
        two_hundred_button.grid(row=1, column=1, pady=5)

        three_hundred_button = tk.Button(button_frame,
                                         text='300',
                                         command=lambda: withdraw(300),
                                         relief='raised',
                                         borderwidth=3,
                                         width=50,
                                         height=4)
        three_hundred_button.grid(row=2, column=1, pady=5)

        cash = tk.StringVar()
        other_amount_entry = tk.Entry(button_frame,
                                      textvariable=cash,
                                      width=59,
                                      justify='right')
        other_amount_entry.grid(row=3, column=1, pady=5, ipady=30)

        def exit():
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                text='Exit',
                                command=exit,
                                font=('orbitron', 10, 'bold'),
                                fg='white', bg='orange',
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=4)
        exit_button.grid(row=4, column=1, pady=5)

        def other_amount(_):
            global current_balance
            amount = int(cash.get())
            hello = check_for_possible_withdraw(current_balance,amount)
            if hello:
                current_balance -= amount
                notes_dispence(amount)
                try:
                    send_message_to_server(current_balance)
                except:
                    print("withdraw over network unsuccessful")
                controller.shared_data['Balance'].set(current_balance)
                cash.set('')
                msg.showinfo('Information','Please Collect Your Cash!')
                controller.show_frame('MenuPage')

        other_amount_entry.bind('<Return>', other_amount)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()

class DepositPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669900')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Test Bank',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#669900')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#669900')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                      text='Enter amount',
                                      font=('orbitron', 16),
                                      bg='#669900',
                                      fg='white')
        enter_amount_label.pack(pady=10)

        cash = tk.StringVar()
        deposit_entry = tk.Entry(self,
                                 textvariable=cash,
                                 font=('orbitron', 12),
                                 width=22)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            global current_balance
            current_balance += int(cash.get())
            try:
                send_message_to_server(current_balance)
            except:
                print("sending unsuccusses")
            controller.shared_data['Balance'].set(current_balance)
            controller.show_frame('MenuPage')
            cash.set('')

        def deposit_cash1(_):
            global current_balance
            current_balance += int(cash.get())
            try:
                send_message_to_server(current_balance)
            except:
                print("sending unsuccusses")
            controller.shared_data['Balance'].set(current_balance)
            msg.showinfo('Information','Cash Deposited!!')
            controller.show_frame('MenuPage')
            cash.set('')

        enter_button = tk.Button(self,
                                 text='Enter',
                                 command=deposit_cash,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)
        deposit_entry.bind('<Return>', deposit_cash1)
        two_tone_label = tk.Label(self, bg='#33334d')
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()

class BalancePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669900')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Test Bank ',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#669900')
        heading_label.pack(pady=25)

        text_label = tk.Label(self,
                                   text='Your Account Balance is: ',
                                   font=('orbitron', 16, 'bold', 'italic'),
                                   fg='white',
                                   bg='#669900',
                                   anchor='w')
        text_label.config(anchor='center')
        text_label.pack()

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_label = tk.Label(self,
                                 textvariable=controller.shared_data['Balance'],
                                 font=('orbitron', 16),
                                 fg='white',
                                 bg='#669900',
                                 anchor='w')
        balance_label.config(anchor='center')
        balance_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def menu():
            controller.show_frame('MenuPage')

        menu_button = tk.Button(button_frame,
                                command=menu,
                                text='Menu',
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=3)
        menu_button.grid(row=0, column=0, pady=5)

        def exit():
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                text='Exit',
                                command=exit,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=3)
        exit_button.grid(row=1, column=0, pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()

if __name__ == "__main__":
    try:
        nmain()
        threading.Thread(target=listen_for_message_from_server, args=(), daemon=True).start()
    except:
        print("Unsuccessful")


    app = SampleApp()
    app.shared_data['Balance'].set(current_balance)
    app.mainloop()

