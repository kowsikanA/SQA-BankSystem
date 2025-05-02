import pytest
from bank_components import *

class TestAccount:

    def test_initialization(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions =0,
            account_plan = "NP"
        )


        assert account_basic.account_number == "01002"
        assert account_basic.account_name == "John Doe"
        assert account_basic.account_status == "A"
        assert account_basic.account_balance == 100.00
        assert account_basic.account_transactions == 0
        assert account_basic.account_plan == "NP"


    def test_get_fee_no_plan(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )
        assert account_basic.getFee() == 0.10

    def test_get_fee_student_plan(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="SP"
        )
        assert account_basic.getFee() == 0.05

    def test_deposit_transaction(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )

        transaction = type('Transaction', (), {'code':'04', 'amount': 50.00})
        result = account_basic.processTransaction(transaction)
        assert result == True
        assert account_basic.account_balance == 150.00
        assert account_basic.account_transactions == 1

    def test_withdraw_transaction(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )
        transaction = type('Transaction', (), {'code':'01', 'amount': 50.00})
        result = account_basic.processTransaction(transaction)
        assert result == True
        assert account_basic.account_balance == pytest.approx(49.90)
        assert account_basic.account_transactions == 1

    def test_transfer_valid(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )
        transaction = type('Transaction', (), {'code': '02', 'amount': 50.00})
        result = account_basic.processTransaction(transaction)
        assert result == True
        assert account_basic.account_balance == 50.00
        assert account_basic.account_transactions == 1

    def test_deactivate_account(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )
        transaction = type('Transaction', (), {'code': '06', 'amount': 50.00})
        result = account_basic.processTransaction(transaction)
        assert result == True
        assert account_basic.account_status == "D"
        assert account_basic.account_transactions == 1

    def test_plan_change(self):
        account_basic = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )
        account_special= Account(
            account_number="01002",
            account_name="Jason Smith",
            account_status="A",
            account_balance=100.00,
            account_transactions=0,
            account_plan="SP"
        )
        transaction = type('Transaction', (), {'code': '08', 'amount': 0.00})

        result = account_basic.processTransaction(transaction)
        assert result == True
        assert account_basic.account_plan == "SP"

        result = account_special.processTransaction(transaction)
        assert result == True
        assert account_special.account_plan == "NP"

    def test_transaction_deactivated(self):
        account_deactivate = Account(
            account_number="01002",
            account_name="John Doe",
            account_status="D",
            account_balance=100.00,
            account_transactions=0,
            account_plan="NP"
        )
        deposit_transaction  =type('Transaction', (), {'code': '04', 'amount': 50.00})
        result = account_deactivate.processTransaction(deposit_transaction)
        assert result == False

        withdraw_transaction = type('Transaction', (), {'code': '01', 'amount': 50.00})
        result = account_deactivate.processTransaction(withdraw_transaction)
        assert result == False

        transfer_transaction = type('Transaction', (), {'code': '02', 'amount': 50.00})
        result = account_deactivate.processTransaction(transfer_transaction)
        assert result == False
