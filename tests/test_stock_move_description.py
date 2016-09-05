# This file is part stock_move_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends
from trytond.tests.test_tryton import doctest_setup, doctest_teardown


class StockMoveDescriptionTestCase(unittest.TestCase):
    'Test Stock Move Description module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('stock_move_description')

    def test0005views(self):
        'Test views'
        test_view('stock_move_description')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockMoveDescriptionTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_stock_move_description.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
