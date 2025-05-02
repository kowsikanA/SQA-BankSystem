import bank_components

"""Main banking system coordinating components"""
class BankSystem:
    def __init__(self):
        self.accountManager = bank_components.AccountManager()
        self.transactionLoader = bank_components.FileLoader()
        self.errorLogger = bank_components.ErrorLogger()

    """Main execution flow"""
    def run(self):
        self.accountManager.loadAccounts('old_master_acc.txt')
        self.accountManager.loadAccounts('merged_acc_transaction.txt')
        self.processTransactions()
        self.accountManager.saveCurrentAccounts('new_current_acc.txt')
        self.accountManager.saveMasterAccounts('new_master_acc.txt')

    """Process all loaded transactions"""
    def processTransactions(self):
        for transaction in self.transactionLoader.getTransactions():
            if not self.accountManager.executeTransaction(transaction):
                self.errorLogger.errorTransaction("Constraint Violation",
                                                  f"Transaction {transaction.code} failed")