# Copyright 2024 Gil Arasa Verge (WVBS.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    automatic_package_creation_mode = fields.Selection(
        selection_add=[
            ("bom_phantom", "Bill of materials Kit")
        ],
    )

    # automatic_package_creation_mode_trigger = fields.Selection([
    #         ("on_done", "On Action Done"),
    #         ("on_prepare", "On Prepare Stock Moves")
    # ])