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
    """ muhasebeye alınacak
    tax_selection_purchase = fields.Many2one('account.tax', string="Tax Selection", help="Select taxes to confirm and apply to all order lines." ,store=True)
    """
    """ Multi Company, Inter company yapısı değişeceği için burası incelenecek
    def _inter_company_create_sale_order(self, dest_company):
        super(PurchaseOrder, self)._inter_company_create_sale_order(dest_company)

        # Satın almadan satışa aktarılacak verileri alın
        purchase_order = self.env['purchase.order'].browse(self.id)

        project = purchase_order.project_purchase
        if project and hasattr(project, 'analytic_account_id') and project.analytic_account_id:
            analytic_account_id = project.analytic_account_id.id
        else:
            analytic_account_id = False

        # Şirket ve partner koşulları
        if purchase_order.company_id.id == 2 and purchase_order.partner_id.id == 1:
            # Satış siparişi değerleri
            sale_order_vals = {
                'project_sales': project.id if project else False,
                'analytic_account_id': analytic_account_id,
                'customer_reference': purchase_order.customer_reference,
            }

            # Satış siparişini bulun
            sale_order = self.env['sale.order'].search([('auto_purchase_order_id', '=', self.id)], limit=1)
            sale_order.write(sale_order_vals)

            # Satın alma siparişi satırlarını döngüleyin ve satış siparişi satırlarını güncelleyin
            for po_line, so_line in zip(purchase_order.order_line, sale_order.order_line):
                sale_line_vals = {
                    'price_unit': po_line.price_unit,
                }
                so_line.write(sale_line_vals)
    """
    """ ID'ler değişecek """
    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id.id == 1:
            self.incoterm_id = 14
        elif self.company_id.id == 2:
            self.incoterm_id = 10
            
    @api.onchange('project_purchase')
    def _onchange_project_purchase(self):
        analytic_account = self.project_purchase.analytic_account_id
        for line in self.order_line:
            line.account_analytic_id = analytic_account.id
    """ Transfer ile ilgili fieldlar burada eklenecek """
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.order_line.write({'production_status': 'tobe_material_purchase'})
            delivery_orders = self.env['stock.picking'].search(
                [('origin', '=', order.name)])
            for delivery_order in delivery_orders:
                delivery_order.write({
                    'project_transfer': [(6, 0, order.project_purchase.ids)],
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

    """kalkıyor
    line_status = fields.Char(string="Line Status")
    """
    delivery_date = fields.Date(string="Required Delivery Date")
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        store=True
    )
    tags = fields.Many2many(related='order_id.tags', string="Tags", readonly=True)
    """kalkıyor
    status = fields.Char(string="Status")
    """
    """Bu ne
    user_id = fields.Char(string="User", related='order_id.user_id.name', readonly=True)
    """
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
    """last_Date Manuel elle doldurulan bir yer kalacak """
    last_date = fields.Date(string="Son Tarih")
    
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