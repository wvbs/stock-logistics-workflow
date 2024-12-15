# Copyright 2024 Gil Arasa Verge (WVBS.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase

class TestAutomaticPackage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test",
                "type": "product",
            }
        )
        cls.product_packaging = cls.env["product.packaging"].create(
            {
                "name": "Box",
                "qty": "2",
                "product_id": cls.product.id,
            }
        )
        cls.product_delivery = cls.env["product.product"].create(
            {
                "name": "Delivery Test",
                "type": "service",
            }
        )
        cls.stock = cls.env.ref("stock.stock_location_stock")
        cls.customers = cls.env.ref("stock.stock_location_customers")
        cls.env["stock.quant"]._update_available_quantity(
            cls.product,
            cls.stock,
            10,
        )
        cls.picking = cls._create_picking()
        cls.picking.move_ids.update({"quantity_done": 5.0})

    @classmethod
    def _create_picking(cls):
        vals = {
            "location_id": cls.stock.id,
            "location_dest_id": cls.customers.id,
            "picking_type_id": cls.env.ref("stock.picking_type_out").id,
            "move_ids": [
                (
                    0,
                    0,
                    {
                        "name": "Product Test",
                        "location_id": cls.stock.id,
                        "location_dest_id": cls.customers.id,
                        "product_id": cls.product.id,
                        "product_uom_qty": 5.0,
                        "product_uom": cls.product.uom_id.id,
                    },
                )
            ],
        }
        return cls.env["stock.picking"].create(vals)

