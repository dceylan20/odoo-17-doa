from odoo import api, fields, models

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'
    _description = "Batch Transfer"
    _order = "name desc"

#fields:

    vehicle_type_id = fields.Many2one('vehicle.type', string='Araç Türü')
    vehicle_id = fields.Char(string='Vehicle Id', inverse='_inverse_maritimetransport_fields')
    transport_equipment_id = fields.Char(string='Transport Equipment "Trailer" Plate Id', inverse='_inverse_transport_equipment_id') #römork plakasını tutmak için mi?
    rail_car_id = fields.Char(string='Rail Car Id', inverse='_inverse_rail_car_id')

    maritimetransport = fields.Boolean(string='Maritime Transport', inverse='_inverse_maritimetransport_fields')
    vessel_name = fields.Char(string='Vessel Name', inverse='_inverse_maritimetransport_fields') #geminin ismi mi plakası mı tutulmalı? name unique mi?
    radio_call_sign_id = fields.Char(string='Radio Call Sign ID', inverse='_inverse_maritimetransport_fields')
    ships_requirements = fields.Text(string='Ships Requirements', inverse='_inverse_maritimetransport_fields')
    gross_tonnage_measure = fields.Float(string='Gross Tonnage Measure', inverse='_inverse_maritimetransport_fields')
    net_tonnage_measure = fields.Float(string='Net Tonnage Measure', inverse='_inverse_maritimetransport_fields')
    registry_cert_doc_ref = fields.Char(string='Registry Certificate Document Reference', inverse='_inverse_maritimetransport_fields')
    registry_port_location = fields.Char(string='Registry Port Location', inverse='_inverse_maritimetransport_fields')

    project_ids = fields.Many2many('project.project', string='Projects', compute='_compute_projects', store=True)
    #purchase.py'de tanımlanacak, purchase_count'u başka yerlerden silebilirsin
    purchase_count = fields.Integer(string='Purchases', compute='_compute_purchase_count')
    scheduled_date = fields.Datetime(string='Scheduled Date')  #bu neden datetime da arrival sadece date?
    arrival_date = fields.Date(string='Arrival Date')
    logistic_company = fields.Many2one('res.partner', inverse='_inverse_logistic_company', string='Logistic Company', domain=[('is_company', '=', True)])
    airtag_url = fields.Char(string='Airtag URL', compute='_compute_airtag_url', store=True)  # Hesaplanmış URL alanı
    import_decleration_number = fields.Char(string='Custom Decleration No', inverse='_inverse_import_decleration_number', store=True)
    sale_numbers = fields.Char(compute='_compute_sale_numbers', string='Sale Numbers')
    unique_countries = fields.Char(compute='_compute_customer_countries', string='Customer Countries') 
    
    situation = fields.Selection(
        [("to_be_planned", "To Be Planned"),
         ("on_the_way", "On The Way"),
         ("arrived", "Arrived")],
        string="Situation",
        store=True,
        inverse='_inverse_situation'
    )
    transport_type = fields.Selection([   #hem vehicle type id var hem transport type var. ikisinden birini silebiliriz bence.
        ('airtransport', 'Air Transport'),
        ('roadtransport', 'Road Transport'),
        ('railtransport', 'Rail Transport'), 
        ('maritimetransport', 'Maritime Transport'),
    ], string='Transport Type',  default="roadtransport", inverse='_inverse_transport_type'
    )
    customer_ids = fields.Many2many(  
        'res.partner',
        'batch_customer_rel',   
        'batch_id', 
        'partner_id', 
        string='Customers'
    )
    vendor_ids = fields.Many2many( 
        'res.partner',
        'batch_vendor_rel', 
        'batch_id',  
        'partner_id', 
        string='Vendors'
    )
    transportation_code = fields.Char(
        string='Transportation Code',
        inverse='_inverse_transportation_code' 
    )    
    driver_ids = fields.Many2many(
        'res.partner',
        'batch_driver_rel',
        'batch_id',
        'partner_id',  
        string='Drivers',
        inverse='_inverse_driver_ids',
        store=True, 
    )

#compute fonsiyonları:

    def _compute_sale_numbers(self):
        for batch in self:
            sale_orders = batch.picking_ids.mapped('sale_id')
            batch.sale_numbers = ', '.join(sale_orders.mapped('name'))  

    def _compute_customer_countries(self):
        for batch in self:
            countries = batch.customer_ids.mapped('country_id').mapped('name')
            unique_countries = list(set(countries))
            batch.unique_countries=', '.join(unique_countries)    

    @api.depends('picking_ids.project_transfer')
    def _compute_projects(self):
        for record in self:
            # Her bir picking kaydındaki project_transfer alanını topla
            projects = record.picking_ids.mapped('project_transfer')
            # Many2many alanına bu projelerin ID'lerini ata
            project_ids = projects.ids if projects else []
            record.project_ids = [(6, 0, project_ids)]

    def _compute_purchase_count(self): 
        for batch in self:
            purchases = self.env['purchase.order'].search([
                ('project_purchase', '=', batch.name) #project_purchase'ı değiştirmen lazım, böyle bir şey yok hatası veriyor
            ])
            batch.purchase_count = len(purchases)

    @api.depends('transportation_code')
    def _compute_airtag_url(self): #transporation kodunu urlinin sonuna ekleyip unique yapıyo
        base_url = "https://portal-test.yenaengineering.nl/transfers/"
        for record in self:
            if record.transportation_code:
                record.airtag_url = base_url + record.transportation_code
            else:
                record.airtag_url = False 


#inverse fonsiyonları:
    
    def _inverse_logistic_company(self):
        for batch in self:
            batch.picking_ids.write({'logistic_company': batch.logistic_company})    

    def _inverse_situation(self):
        for batch in self:
            batch.picking_ids.write({'situation': batch.situation})  

    @api.depends('picking_ids.transport_type')   #bu apilere gerek var mı inverse methodda
    def _inverse_transport_type(self):
        for batch in self:
            batch.picking_ids.write({'transport_type': batch.transport_type})

    @api.depends('picking_ids.transport_equipment_id') 
    def _inverse_transport_equipment_id(self):
        for batch in self:
            batch.picking_ids.write({'transport_equipment_id': batch.transport_equipment_id})
    
    @api.depends('picking_ids.rail_car_id')  
    def _inverse_rail_car_id(self):
        for batch in self:
            batch.picking_ids.write({'rail_car_id': batch.rail_car_id})

    @api.depends('picking_ids.vessel_name', 'picking_ids.radio_call_sign_id', 
                 'picking_ids.ships_requirements', 'picking_ids.gross_tonnage_measure', 
                 'picking_ids.net_tonnage_measure', 'picking_ids.registry_cert_doc_ref', 
                 'picking_ids.registry_port_location', 'picking_ids.vehicle_id')
    def _inverse_maritimetransport_fields(self): 
        for batch in self:
            batch.picking_ids.write({
                'vessel_name': batch.vessel_name,
                'radio_call_sign_id': batch.radio_call_sign_id,
                'ships_requirements': batch.ships_requirements,
                'gross_tonnage_measure': batch.gross_tonnage_measure,
                'net_tonnage_measure': batch.net_tonnage_measure,
                'registry_cert_doc_ref': batch.registry_cert_doc_ref,
                'registry_port_location': batch.registry_port_location,
                'vehicle_id': batch.vehicle_id,
            }) 

    def _inverse_import_decleration_number(self):
        for batch in self:
            if batch.import_decleration_number:
                batch.picking_ids.write({'import_decleration_number': batch.import_decleration_number})

    @api.depends('picking_ids.driver_ids')
    def _inverse_driver_ids(self):
        for batch in self:
            driver_ids = batch.driver_ids.ids
            batch.picking_ids.write({'driver_ids': [(6, 0, driver_ids)]})

    def _inverse_transportation_code(self):   #set_transportation_code olarak yazılmıştı ama fieldda _inverse yazılmıştı değiştirdim ismini.
        for batch in self:
            transportation_code = batch.transportation_code
            for picking in batch.picking_ids:
                picking.transportation_code = transportation_code
                picking.message_post(body="Transportation code updated to {}".format(transportation_code)) #updatelenince mesaj gidiyor   


#action fonksiyonları:
    
    def action_show_purchases(self): #batche ait purchasesı göster
        self.ensure_one()
        purchase_ids = []

        # Batch transferin adı ile eşleşen purchase'ları bul
        purchases = self.env['purchase.order'].search([('project_purchase', '=', self.name)]) #burada hata veriyor

        for purchase in purchases:
            purchase_ids.append(purchase.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', purchase_ids)],
            'context': {'create': True},
        }
    
    def action_batch_despatch_send(self):
        self.ensure_one()  #her kayıttan bir tane olduğundan emin olmak için
        for picking in self.picking_ids:
            if hasattr(picking, 'action_despatch_send'):
                picking.action_despatch_send()  


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    project_ids = fields.Many2many('project.project', string='Projects', compute='_compute_project_transfer', store=True)

    @api.depends('picking_id.project_transfer')
    def _compute_project_transfer(self):
        for record in self:
            record.project_ids = record.picking_id.project_transfer 


class Picking(models.Model):
    _inherit = 'stock.picking'
    project_transfer = fields.Many2many("project.project", string="Project Number", store=True) 
    effective_date = fields.Date(string="Effective Date", store=True) #bu ne niye var?
    arrival_date = fields.Date(related="batch_id.arrival_date", string='Arrival Date' ,store=True, readonly=False)
    logistic_company = fields.Many2one('res.partner', string='Logistic Company', domain=[('is_company', '=', True)])
    situation = fields.Selection(
        [("to_be_planned", "To Be Planned"),
         ("on_the_way", "On The Way"),
         ("arrived", "Arrived")],
        string="Situation",
        store=True,
        readonly=False
    )
    transportation_code = fields.Char(
        string="Transportation Code",
        store=True,
        readonly=False
    )
    
    def write(self, vals): 
        res = super().write(vals)
        if 'batch_id' in vals:
            for record in self:
                if record.batch_id:
                    record.situation = record.batch_id.situation
        return res
        
    def _create_backorder(self): # yedek sipariş oluştururken transportation kodunu '-' yapıyor
        backorder_picking = super()._create_backorder()
        if backorder_picking:
            backorder_picking.transportation_code = '-'
        return backorder_picking
