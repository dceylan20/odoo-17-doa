from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    rfq_sent_date = fields.Date(string="S-RFQ Sent Date")
    rfq_date = fields.Date(string="S-RFQ Date")
    delivery_date = fields.Date(string="Required Delivery Date")
    customer_reference = fields.Char(string="Customer Reference No", store=True)
    project_purchase = fields.Many2one('project.project', string="Project Number", store=True)
    contact_id = fields.Many2one('res.partner', string='Contact Person', store=True)
    tags = fields.Many2many("project.tags", string="Tags")
    


    def _inter_company_create_sale_order(self, dest_company):
        super(PurchaseOrder, self)._inter_company_create_sale_order(dest_company)
        project = self.project_purchase
        analytic_account_id = project.analytic_account_id.id if project and project.analytic_account_id else False

        if self.company_id.id == 2 and self.partner_id.id == 1:
            sale_order = self.env['sale.order'].search([('auto_purchase_order_id', '=', self.id)], limit=1)
            sale_order_vals = {
                'project_sales': project.id if project else False,
                'analytic_account_id': analytic_account_id,
                'customer_reference': self.customer_reference,
            }
            sale_order.write(sale_order_vals)

            for po_line, so_line in zip(self.order_line, sale_order.order_line):
                so_line.write({'price_unit': po_line.price_unit})

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.incoterm_id = 14 if self.company_id.id == 1 else 10 if self.company_id.id == 2 else self.incoterm_id

    @api.onchange('project_purchase')
    def _onchange_project_purchase(self):
        analytic_account = self.project_purchase.analytic_account_id
        for line in self.order_line:
            line.account_analytic_id = analytic_account.id if analytic_account else False

    def button_confirm(self):
        locked = fields.Boolean(default=True) 
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.order_line.write({'production_status': 'tobe_material_purchase'})
            delivery_orders = self.env['stock.picking'].search([('origin', '=', order.name)])
            for delivery_order in delivery_orders:
                delivery_order.write({
                    'project_transfer': [(6, 0, [order.project_purchase.id])],
                })
        return res

    def button_cancel(self):
        res = super(PurchaseOrder, self).button_cancel()
        for order in self:
            order.order_line.write({'production_status': False})
        return res

    def mark_as_sent(self):
        for record in self:
            record.write({
                'rfq_sent_date': fields.Date.today(),
                'state': 'sent',
            })

    @api.onchange('delivery_date')
    def _onchange_delivery_date(self):
        for line in self.order_line:
            line.delivery_date = self.delivery_date

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.contact_id = False
        return {'domain': {'contact_id': [('parent_id', '=', self.partner_id.id), ('type', '=', 'contact')]}}


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    project_purchase = fields.Many2one(
        'project.project',
        related='order_id.project_purchase',
        string="Project Purchase",
        store=True,
        readonly=True
    )
    delivery_date = fields.Date(string="Required Delivery Date")
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        store=True
    )
    tags = fields.Many2many(related='order_id.tags', string="Tags", readonly=True)

    production_status = fields.Selection([
        ('tobe_material_purchase', 'To be Material Purchase'),
        ('material_purchase', 'Material Purchased'),
        ('tobe_cut', 'To be Cut'),
        ('cutting', 'Cutting'),
        ('tobe_bend', 'To Be Bend'),
        ('bending', 'Bending'),
        ('tobe_weld', 'To Be Weld'),
        ('welding', 'Welding'),
        ('tobe_sand_blast', 'To Be Sand Blast'),
        ('sand_blasting', 'Sand Blasting'),
        ('tobe_painting', 'To be Paint'),
        ('painting', 'Painting'),
        ('tobe_hd_galvanize', 'To be Hot Dip Galvanize'),
        ('hd_galvanizing', 'Hot Dip Galvanizing'),
        ('tobe_e_galvanize', 'To be Electro Galvanize'),
        ('e_galvanizing', 'Electro Galvanizing'),
        ('tobe_package', 'To be Package'),
        ('packing', 'Packaging'),
        ('ready', 'Ready'),
        ('metalworks', 'Metalworks'),
        ('attention', 'Attention'),
        ('attention_repair', 'Attention Repair'),
        ('despatched', 'Despatched'),
        ('partially_despatched', 'Partially Despatched'),
        ('whoops', 'WHOOPS!'),
    ], string='Production Status')

    last_date = fields.Date(string="Last Date")

    @api.onchange('qty_received', 'product_qty')
    def _onchange_production_status(self):
        for record in self:
            if record.qty_received == record.product_qty and record.product_qty > 0:
                new_status = 'despatched'
            elif 0 < record.qty_received < record.product_qty:
                new_status = 'partially_despatched'
            elif record.qty_received > record.product_qty:
                new_status = 'whoops'
            else:
                new_status = record.production_status

            if new_status != record.production_status:
                record.production_status = new_status
