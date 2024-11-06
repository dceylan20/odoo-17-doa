# -*- coding: utf-8 -*-
# from odoo import http


# class SupplierClassification(http.Controller):
#     @http.route('/supplier_classification/supplier_classification', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/supplier_classification/supplier_classification/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('supplier_classification.listing', {
#             'root': '/supplier_classification/supplier_classification',
#             'objects': http.request.env['supplier_classification.supplier_classification'].search([]),
#         })

#     @http.route('/supplier_classification/supplier_classification/objects/<model("supplier_classification.supplier_classification"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('supplier_classification.object', {
#             'object': obj
#         })

