import unittest
import budget
from budget import create_spend_chart


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.food = budget.Category("Food")
        self.entertainment = budget.Category("Entertainment")
        self.business = budget.Category("Business")

    def test_deposit(self):
        self.food.deposit(900, "deposit")
        actual = self.food.ledger[0]
        expected = {"amount": 900, "description": "deposit"}
        self.assertEqual(actual, expected, 'Expected `deposit` method to create a specific object in the ledger instance variable.')

    def test_deposit_no_description(self):
        self.food.deposit(45.56)
        actual = self.food.ledger[0]
        expected = {"amount": 45.56, "description": ""}
        self.assertEqual(actual, expected, 'Expected calling `deposit` method with no description to create a blank description.')

    def test_withdraw(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        actual = self.food.ledger[1]
        expected = {"amount": -45.67, "description": "milk, cereal, eggs, bacon, bread"}
        self.assertEqual(actual, expected, 'Expected `withdraw` method to create a specific object in the ledger instance variable.')

    def test_withdraw_no_description(self):
        self.food.deposit(900, "deposit")
        good_withdraw = self.food.withdraw(45.67)
        actual = self.food.ledger[1]
        expected = {"amount": -45.67, "description": ""}
        self.assertEqual(actual, expected, 'Expected `withdraw` method with no description to create a blank description.')
        self.assertEqual(good_withdraw, True, 'Expected `transfer` method to return `True`.')

    def test_get_balance(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        actual = self.food.get_balance()
        expected = 854.33
        self.assertEqual(actual, expected, 'Expected balance to be 854.33')

    def test_transfer(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        good_transfer = self.food.transfer(20, self.entertainment)
        actual = self.food.ledger[2]
        expected = {"amount": -20, "description": "Transfer to Entertainment"}
        self.assertEqual(actual, expected, 'Expected `transfer` method to create a specific ledger item in food object.')
        self.assertEqual(good_transfer, True, 'Expected `transfer` method to return `True`.')
        actual = self.entertainment.ledger[0]
        expected = {"amount": 20, "description": "Transfer from Food"}
        self.assertEqual(actual, expected, 'Expected `transfer` method to create a specific ledger item in entertainment object.')

    def test_check_funds(self):
        self.food.deposit(10, "deposit")
        actual = self.food.check_funds(20)
        expected = False
        self.assertEqual(actual, expected, 'Expected `check_funds` method to be False')
        actual = self.food.check_funds(10)
        expected = True
        self.assertEqual(actual, expected, 'Expected `check_funds` method to be True')

    def test_withdraw_no_funds(self):
        self.food.deposit(100, "deposit")
        good_withdraw = self.food.withdraw(100.10)
        self.assertEqual(good_withdraw, False, 'Expected `withdraw` method to return `False`.')

    def test_transfer_no_funds(self):
        self.food.deposit(100, "deposit")
        good_transfer = self.food.transfer(200, self.entertainment)
        self.assertEqual(good_transfer, False, 'Expected `transfer` method to return `False`.')
