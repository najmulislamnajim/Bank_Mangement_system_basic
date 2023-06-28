from datetime import datetime

class Bank:
    __total_balance=0
    __loan_amount=0
    def __init__(self) -> None:
        pass
    
    def get_bank_balance(self):
        return Bank.__total_balance
    
    def show_bank_balance(self):
        print(f'Total balance is {Bank.__total_balance} tk.')

    def update_balance(self,amount):
        Bank.__total_balance+=amount

    def update_loan(self,amount):
        Bank.__loan_amount+=amount
    
    def get_loan_amount(self):
        return self.__loan_amount


class History:
    def __init__(self,amount,transaction_type) -> None:
        self.date=datetime.now().strftime('%d-%m-%y')
        self.time=datetime.now().strftime('%H:%M')
        self.amount=amount
        self.type=transaction_type

class Loan():
    __status=1
    def __init__(self) -> None:
        pass

    def get_status(self):
        return Loan.__status
    
    def update_status(self,value):
        Loan.__status=value

class User(Bank):
    def __init__(self,name,email,password) -> None:
        super().__init__()
        self.user_name=name
        self.user_email=email
        self.__user_password=password
        self.__user_balance=0
        self.transaction_history=[]

    def create_account(self):
        user={'name':self.user_name,'E-mail':self.user_email,'Password':self.__user_password}
        return user

    def deposit(self,amount):
        if amount>0:
            self.__user_balance+=amount
            self.update_balance(amount)
            history=History(amount,'diposit')
            self.transaction_history.append(history)
        else:
            print(f'You can\'t deposit zero or negative balance')

    def withdraw(self,amount):
        if amount<=0:
            print(f'You can\'t withdraw zero or negative balance')
        elif amount<=self.__user_balance:
            balance_of_bank=self.get_bank_balance()
            if amount<=balance_of_bank:
                self.__user_balance-=amount
                self.update_balance(amount*-1)
                history=History(amount,'withdraw')
                self.transaction_history.append(history)
                withdraw_message=f'''
                    {amount} tk withdraw successfully from your '{self.user_name}' acoount.
                    Your current balance is {self.__user_balance}.
                '''
                print(withdraw_message)
            else:
                print(f'The bank is bankrupt.')

    def transfer_money(self,amount,transfer_to):
        if amount<=0:
           print(f'You can\'t transfer zero or negative balance')
        elif amount>self.get_bank_balance():
            print(f'The bank is bankrupt. You can\'t transfer money now!')
        elif amount<=self.__user_balance:
            # update balance
            self.__user_balance-=amount
            transfer_to.__user_balance+=amount

            # update transaction history
            history1=History(amount,'send money')
            history2=History(amount,'recieved money')
            self.transaction_history.append(history1)
            transfer_to.transaction_history.append(history2)

            # give a message
            transaction_message=f'''
                Successfully transfered {amount} tk from {self.user_name} to {transfer_to.user_name}.
            '''
            print(transaction_message)
        else:
            print(f'Insufficient Balance.')

    def get_transaction_history(self):
        print(f'                ======> Transaction History <======')
        for x in self.transaction_history:
            text=f'''
                {x.date} {x.time} {x.type} {x.amount} tk.
            '''
            print(text)
        print(f'                        ======> end <======')
        print()

    def get_transaction_history_by_date(self,date):
        date=str(date)
        print(f'                ======> Transaction History <======')
        for x in self.transaction_history:
            if date in x.date:
                text=f'''
                {x.date} {x.time} {x.type} {x.amount} tk.
            '''
            print(text)
        print(f'                        ======> end <======')
        print()

    def take_loan(self,amount):
        if amount>2*self.__user_balance:
            print(f'too much tk you want')
        elif amount<=0:
            print(f'You can\'t take zero or negative balance as loan.')
        elif amount>self.get_bank_balance():
            print(f'The bank is bankrupt.')
        else:
            loan=Loan()
            if loan.get_status()==1:
                #self.update_balance(amount)
                self.__user_balance+=amount
                self.update_loan(amount)
                loan_message=f'''
                    You got {amount} tk loan.
                '''
                history=History(amount,'loan')
                self.transaction_history.append(history)
                print(loan_message)
            else:
                print(f'Currently, our loan system has off.')

    def send_money(self,amount,user):
        self.transfer_money(amount,user)

    def check_available_balance(self):
        print(f'{self.user_name} has {self.__user_balance} tk.')


class Admin(Bank,Loan):
    def __init__(self,name,email,password) -> None:
        super().__init__()
        self.admin_name=name
        self.admin_email=email
        self.__admin_password=password

    def create_account(self):
        user={'name':self.admin_name,'E-mail':self.admin_email,'Password':self.__admin_password}
        return user

    def check_available_balance(self):
        available_balance=self.get_bank_balance()
        print(f'Bank total balance is {available_balance} tk.')

    def check_loan_amount(self):
        loan_amount=self.get_loan_amount()
        print(f'Bank has total {loan_amount} tk. loan.')

    def turn_on_loan_feature(self):
        self.update_status(1)
    
    def turn_off_loan_feature(self):
        self.update_status(0)

user1=User('Najmul','nin@gmail.com','Najmul')
user1.deposit(4746879)
user1.withdraw(2554)
user1.check_available_balance()
Bank.show_bank_balance(Bank)

user2=User('Najim','najim@gmail.com','Najim')
user2.check_available_balance()
Bank.show_bank_balance(Bank)
user1.transfer_money(5000,user2)
user2.check_available_balance()
user1.check_available_balance()
Bank.show_bank_balance(Bank)

user1.get_transaction_history()
user2.get_transaction_history_by_date(28)

user2.take_loan(522)
user2.check_available_balance()
Bank.show_bank_balance(Bank)

admin=Admin('sufian','sf@gmail.com','suf')
admin.check_available_balance()
admin.check_loan_amount()
admin.turn_off_loan_feature()
user1.take_loan(500)
admin.turn_on_loan_feature()
user1.take_loan(5000)
