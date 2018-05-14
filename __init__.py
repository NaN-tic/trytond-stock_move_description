# This file is part stock_move_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import stock
from . import sale
from . import purchase


def register():
    Pool.register(
        stock.Move,
        stock.ShipmentOut,
        stock.ShipmentIn,
        module='stock_move_description', type_='model')
    Pool.register(
        purchase.PurchaseLine,
        depends=['purchase'],
        module='stock_move_description', type_='model')
    Pool.register(
        sale.SaleLine,
        depends=['sale'],
        module='stock_move_description', type_='model')
