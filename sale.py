# This file is part stock_move_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['SaleLine']


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    def get_move(self, shipment_type):
        # copy description from sale to shipment
        move = super(SaleLine, self).get_move(shipment_type)

        if move:
            move.description = self.description

        return move
