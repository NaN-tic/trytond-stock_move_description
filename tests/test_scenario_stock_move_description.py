import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import create_chart, get_accounts
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install stock_move_description Module
        config = activate_modules(
            ['stock_move_description', 'sale', 'purchase'])

        # Create company
        _ = create_company()
        company = get_company()
        tax_identifier = company.party.identifiers.new()
        tax_identifier.type = 'eu_vat'
        tax_identifier.code = 'BE0897290877'
        company.party.save()

        # Reload the context
        User = Model.get('res.user')
        config._context = User.get_preferences(True, config.context)

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create parties
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.save()

        # Create account category
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        Product = Model.get('product.product')
        product = Product()
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.purchasable = True
        template.salable = True
        template.list_price = Decimal('10')
        template.cost_price_method = 'fixed'
        template.account_category = account_category
        template.save()
        product.template = template
        product.save()

        # Create payment term
        PaymentTerm = Model.get('account.invoice.payment_term')
        payment_term = PaymentTerm(name='Term')
        payment_term.lines.new(type='remainder')
        payment_term.save()

        # Create a Sale
        Sale = Model.get('sale.sale')
        SaleLine = Model.get('sale.line')
        sale = Sale()
        sale.party = party
        sale.payment_term = payment_term
        sale.invoice_method = 'manual'
        sale_line = SaleLine()
        sale.lines.append(sale_line)
        sale_line.product = product
        sale_line.quantity = 2.0
        sale_line.description = 'Product Description'
        sale.save()
        Sale.quote([sale.id], config.context)
        Sale.confirm([sale.id], config.context)
        Sale.process([sale.id], config.context)
        self.assertEqual(sale.state, 'processing')
        sale.reload()
        shipment, = sale.shipments
        outgoing_move, = shipment.outgoing_moves
        self.assertEqual(outgoing_move.description, 'Product Description')
        inventory_move, = shipment.inventory_moves
        self.assertEqual(inventory_move.description, 'Product Description')

        # Create a Return Sale
        Sale = Model.get('sale.sale')
        SaleLine = Model.get('sale.line')
        sale = Sale()
        sale.party = party
        sale.payment_term = payment_term
        sale.invoice_method = 'manual'
        sale_line = SaleLine()
        sale.lines.append(sale_line)
        sale_line.product = product
        sale_line.quantity = -1.0
        sale_line.description = 'Product Description'
        sale.save()
        Sale.quote([sale.id], config.context)
        Sale.confirm([sale.id], config.context)
        Sale.process([sale.id], config.context)
        self.assertEqual(sale.state, 'processing')
        sale.reload()
        shipment, = sale.shipment_returns
        incoming_move, = shipment.incoming_moves
        self.assertEqual(incoming_move.description, 'Product Description')

        # Create a Purchase
        Purchase = Model.get('purchase.purchase')
        PurchaseLine = Model.get('purchase.line')
        purchase = Purchase()
        purchase.party = party
        purchase.payment_term = payment_term
        purchase.invoice_method = 'manual'
        purchase_line = PurchaseLine()
        purchase.lines.append(purchase_line)
        purchase_line.product = product
        purchase_line.quantity = 2.0
        purchase_line.description = 'Product Description'
        purchase_line.unit_price = product.cost_price
        purchase.save()
        Purchase.quote([purchase.id], config.context)
        Purchase.confirm([purchase.id], config.context)
        Purchase.process([purchase.id], config.context)
        self.assertEqual(purchase.state, 'processing')
        purchase.reload()
        move, = purchase.moves
        self.assertEqual(move.description, 'Product Description')
