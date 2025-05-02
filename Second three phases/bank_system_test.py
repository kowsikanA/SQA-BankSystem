import pytest
from bank_components import *
from bank_system import *


class TestBankSystem:
    def test_bank_system_run(self):

        bank = BankSystem()

        result = bank.run()
        assert result

    def test_process_transaction_with_mocks(self):

        manager = AccountManager()
        bank = BankSystem()

        t1 = Transaction("05", "Carol", "00003", 30.0, "")
        manager.executeTransaction(t1)


        assert bank.processTransactions()

        assert True