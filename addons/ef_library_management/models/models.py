# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ef_library_management(models.Model):
#     _name = 'ef_library_management.ef_library_management'
#     _description = 'ef_library_management.ef_library_management'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
