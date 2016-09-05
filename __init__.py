# This file is part stock_move_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .stock import *
from .sale import *
from .purchase import *


def register():
    Pool.register(
        Move,
        ShipmentOut,
        ShipmentIn,
        SaleLine,
        PurchaseLine,
        module='stock_move_description', type_='model')
