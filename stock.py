# This file is part stock_move_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Move', 'ShipmentOut', 'ShipmentIn']


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'
    description = fields.Text('Description')

    @fields.depends('product', 'description', 'shipment')
    def on_change_product(self):
        Product = Pool().get('product.product')

        super(Move, self).on_change_product()

        if self.product:
            party_context = {}
            if self.shipment:
                shipment = self.shipment
                if shipment.__name__ in ['stock.shipment.in']:
                    if shipment.supplier.lang:
                        party_context['language'] = shipment.supplier.lang.code
                if shipment.__name__ in ['stock.shipment.out',
                        'stock.shipment.out.return']:
                    if shipment.customer.lang:
                        party_context['language'] = shipment.customer.lang.code

            if not self.description:
                with Transaction().set_context(party_context):
                    self.description = Product(self.product.id).rec_name


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    def _get_inventory_move(self, move):
        # copy description from outgoing to inventory
        new_move = super(ShipmentOut, self)._get_inventory_move(move)
        new_move.description = move.description
        return new_move


class ShipmentIn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'

    def _get_inventory_move(self, incoming_move):
        # copy description from incoming to inventory
        move = super(ShipmentIn, self)._get_inventory_move(incoming_move)
        move.description = incoming_move.description
        return move


