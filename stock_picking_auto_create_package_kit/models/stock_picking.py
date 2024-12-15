# Copyright 2024 Gil Arasa Verge (WVBS.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
import re

import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_put_in_pack(self):
        self._auto_create_delivery_package()

    def _auto_create_delivery_package(self) -> None:
        res = super()._auto_create_delivery_package()

        if self.picking_type_id.automatic_package_creation_mode == "bom_phantom":
            self._auto_create_delivery_package_bom_phantom()


    def _auto_create_delivery_package_bom_phantom(self) -> None:
        """
        Put each done bom kit in a package like stock.move._compute_description_bom_line() calculates the description
        """
        _logger.info("Starting _auto_create_delivery_package_bom_phantom")

        for picking in self:
            _logger.info(f"Processing picking: {picking.id}")

            new_packages = {}

            for move_line in picking.move_line_ids:
                move_line = self._auto_create_delivery_package_filter(move_line)
                if not move_line:
                    _logger.info("Move line filtered out")
                    continue
                if not move_line.description_bom_line:
                    _logger.info("Move line has no description_bom_line")
                    continue
                
                match = re.match(r"(.+) - (\d+)\/(\d+)", move_line.description_bom_line)
                if not match:
                    _logger.info(f"No match for description_bom_line: {move_line.description_bom_line}")
                    continue

                name, current, total = match.groups()
                current = int(current)
                total = int(total)

                _logger.info(f"Matched name: {name}, current: {current}, total: {total}")

                # Now group all "name" lines together and put them in a package
                if name not in new_packages:
                    new_packages[name] = {
                        "current": 0,
                        "total": total,
                        "lines": []
                    }
                
                _logger.info(f"new_packages: {new_packages}")
                new_packages[name]["current"] += current
                new_packages[name]["lines"].append(move_line)

                if new_packages[name]["current"] == total:
                    _logger.info(f"Packing lines for {name}")
                    picking._put_in_pack(new_packages[name]["lines"])

                    # Clean up so we allow other kits of the same type to be processed
                    del new_packages[name]

        _logger.info("Finished _auto_create_delivery_package_bom_phantom")

    # def _action_done(self):
    #     for rec in self:
    #         rec._auto_create_delivery_package()
    #     return super()._action_done()
