# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Greuceanu
# This file is part of SWTOR Armory and is licensed under the
# GNU Affero General Public License v3.0 or later.
# from odoo import http


# class SwtorArmory(http.Controller):
#     @http.route('/swtor_armory/swtor_armory', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/swtor_armory/swtor_armory/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('swtor_armory.listing', {
#             'root': '/swtor_armory/swtor_armory',
#             'objects': http.request.env['swtor_armory.swtor_armory'].search([]),
#         })

#     @http.route('/swtor_armory/swtor_armory/objects/<model("swtor_armory.swtor_armory"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('swtor_armory.object', {
#             'object': obj
#         })
