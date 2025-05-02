import read
import write
import print_error

"""Represents a bank account with various attributes and transaction processing capabilities"""


class Account:
    def __init__(self, account_number, account_name, account_status, account_balance, account_transactions,
                 account_plan):
        self.account_number = account_number
        self.account_name = account_name
        self.account_status = account_status
        self.account_balance = account_balance
        self.account_transactions = account_transactions
        self.account_plan = account_plan

    """Process different transaction types and update account state"""

    def processTransaction(self, transaction):

        if self.account_status == "D" and transaction.code not in ("07", "00"):
            return False
        if transaction.code == "01":  # WithDrawl
            new_balance = self.account_balance - transaction.amount - self.getFee()
            if new_balance < 0:
                return False
            self.account_balance = new_balance
        elif transaction.code == "02" or transaction.code == "03":  # Transfer
            if self.account_balance - transaction.amount - self.getFee() < 0:
                return False
            self.account_balance -= transaction.amount
        elif transaction.code == "04":
            self.account_balance += transaction.amount
        elif transaction.code == "06":
            self.account_status = "D"
        elif transaction.code == "07":
            self.account_status = "D"
        elif transaction.code == "08":
            if self.account_plan == "SP":
                self.account_plan = "NP"
            else:
                self.account_plan = "SP"
        self.account_transactions += 1
        return True

    """Get transaction fee based on account plan"""

    def getFee(self):
        if self.account_plan == "SP":
            return 0.05
        else:
            return 0.10


class Transaction:
    """Represents a financial transaction with parsing functionality"""

    def __init__(self, code, holder, number, amount, misc):
        self.code = code
        self.holder = holder
        self.number = number
        self.amount = amount
        self.misc = misc

    """Parse transaction from fixed-width string format"""

    def parse(self, transaction_line):
        code = transaction_line[0:2]
        holder = transaction_line[3:23].strip()
        number = transaction_line[24:29].lstrip("0") or "0"
        amount = float(transaction_line[30:38]) if transaction_line[30:38].strip() else 0
        misc = transaction_line[39:].strip()
        return Transaction(code, holder, number, amount, misc)


"""Manages account operations and transaction execution"""


class AccountManager:
    def __init__(self):
        self.accounts = {}

    """Load accounts from file using external read module"""

    def loadAccounts(self, file_path):

        account_list = read.read_old_bank_accounts(file_path)
        for acc in account_list:
            account = Account(
                acc['account_number'],
                acc['name'],
                acc['status'],
                acc['balance'],
                acc['total_transactions'],
                "SP"
            )
            self.accounts[acc['name']] = account

    """Execute transaction based on its type"""

    def executeTransaction(self, transaction):
        if transaction.code == "00":
            return True
        acc = self.getAccount(transaction.number)
        if acc is None and transaction.code != "05":
            return False

        if transaction.code == "05":
            if transaction.number in self.accounts:
                return False
            new_account = Account(transaction.number, transaction.holder, "A", transaction.amount, 0, "NP")
            self.accounts[transaction.number] = new_account
            return True
        return acc.executeTransaction(transaction)

    """Save accounts in master file format"""

    def saveMasterAccounts(self, file_path):

        with open(file_path, 'w') as file:
            for acc in sorted(self.accounts.values(), key=lambda x: x.account_number):
                acc_number = acc.account_number.zfill(5)
                acc_holder = acc.account_name.ljust(20)[:20]
                acc_status = acc.account_status
                acc_balance = f"{acc.account_balance:.2f}"
                acc_transactions = f"{acc.account_transactions:04d}"

                file.write(f"{acc_number} {acc_holder} {acc_status} {acc_balance} {acc_transactions}\n")

    def saveCurrentAccounts(self, file_path):
        account_list = []
        for acc in self.accounts.values():
            account_list.append(
                {
                    'account_number': acc.account_number,
                    'name': acc.account_name,
                    'status': acc.account_status,
                    'balance': acc.account_balance,
                })
        write.write_new_current_accounts(account_list, file_path)

    def getAccount(self, account_number):
        return self.accounts.get(account_number)

    def checkAccountPlan(self, account):
        if account.contains("SP"):
            return "SP"
        else:
            return "NP"


"""Loads transactions from file"""


class FileLoader:
    def __init__(self):
        self.transactions = []

    def setTransactions(self, file_path):
        with open(file_path, "r") as file:
            for l in file:
                line = l.rstrip("\n")
                if len(line) != 40:
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid transaction length: {len(line)}")
                    continue
                self.transactions.append(Transaction.parse(line))

    def getTransactions(self):
        return self.transactions


"""Handles error logging and reporting"""


class ErrorLogger:
    def logError(self, constraint_type, description):
        print_error.log_constraint_error(constraint_type, description)

    def logFatalError(self, msg):
        print(f"ERROR: Fatal error - {msg}")
        exit(1)