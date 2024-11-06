from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    SELECTION_OPTIONS = [
        ('inhouse', 'Inhouse'),
        ('outsource', 'Outsource'),
        ('unable', 'Can NOT do it')
    ]
    RATING =[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
    ]
    creating_changing_design = fields.Selection(SELECTION_OPTIONS, string='Creating/Changing Design')
    creating_changing_design_note = fields.Char(string='Creating/Changing Design Note')

    preparing_shop_drawings = fields.Selection(SELECTION_OPTIONS, string='Preparing Shop Drawings')
    preparing_shop_drawings_note = fields.Char(string='Preparing Shop Drawings Note')

    surface_prep = fields.Selection(SELECTION_OPTIONS, string='Surface Prep.')
    surface_prep_note = fields.Char(string='Surface Prep. Note')

    surface_coating = fields.Selection(SELECTION_OPTIONS, string='Surface Coating')
    surface_coating_note = fields.Many2many('coating', string='Surface Coating Note')

    shipment_in_the_country = fields.Selection(SELECTION_OPTIONS, string='Shipment (in the country)')
    shipment_in_the_country_note = fields.Char(string='Shipment (in the country) Note')

    shipment_between_countries = fields.Selection(SELECTION_OPTIONS, string='Shipment (between countries)') #yoktu ben ekledim, hata verdiği için 
    shipment_between_countries_note = fields.Char(string='Shipment (between countries) Note')

    storing = fields.Selection(SELECTION_OPTIONS, string='Storing')
    storing_note = fields.Char(string='Storing Note')

    blue_collar_number = fields.Float(string='Number of Blue Collar Workers')
    white_collar_number = fields.Float(string='Number of White Collar Workers')
    are_of_expertise = fields.Many2many('area.expertise', string='Area of Expertise')
    comment = fields.Html(string="Comment")

    # Potential vendor alanları
    material_buying = fields.Selection(SELECTION_OPTIONS, string='Material Buying')
    material_buying_note = fields.Char(string='Material Buying Note')

    cutting_drilling = fields.Selection(SELECTION_OPTIONS, string='Cutting, Drilling')
    cutting_drilling_note = fields.Char(string='Cutting, Drilling Note')

    bending = fields.Selection(SELECTION_OPTIONS, string='Bending')
    bending_note = fields.Char(string='Bending Note')

    machining = fields.Selection(SELECTION_OPTIONS, string='Machining')
    machining_note = fields.Char(string='Machining Note')

    welding = fields.Selection(SELECTION_OPTIONS, string='Welding')
    welding_note = fields.Many2many('welding',string='Welding Note')

    quality_control = fields.Selection(SELECTION_OPTIONS, string='Quality Control')
    quality_control_note = fields.Char(string='Quality Control Note')

    packaging = fields.Selection(SELECTION_OPTIONS, string='Packaging')
    packaging_note = fields.Char(string='Packaging Note')

    door_width = fields.Float(string='Door Width')
    door_height = fields.Float(string='Door Height')

    crane_capacity = fields.Float(string='Crane Capacity')
    indoor_area = fields.Float(string='Indoor Area')  #anlamadım bunlar ne için lazım
    outdoor_area = fields.Float(string='Outdoor Area')
    number_of_shifts = fields.Float(string='Number of Shifts/Day')
    machine_equipment_list = fields.Many2many('ir.attachment', 'machine_equipment_list_rel', 'vendor_id', 'attachment_id', string='Machine Equipment List')
    welder_certifications = fields.Many2many('ir.attachment', 'welder_certifications_rel', 'vendor_id', 'attachment_id', string='Welder Certifications') #neden ayrı ayrı tutuyoruz bu sertifikaları
    certifications = fields.Many2many('ir.attachment', 'certifications_rel', 'vendor_id', 'attachment_id', string='Certifications')
    wps_pqr = fields.Many2many('ir.attachment', 'wps_pqr_rel', 'vendor_id', 'attachment_id', string='WPS/PQR')
    final_quality_rating = fields.Selection(RATING, string="Final Product with Desired Quality")
    experience_level = fields.Selection(RATING, string="Knowledge/Experience Level in the Field")
    flexibility = fields.Selection(RATING, string="Flexibility in Special Projects") #ne açıdan?
    welding_skills = fields.Selection(RATING, string="Welding Skills")

    contact_status_customer = fields.Boolean(compute='_compute_contact_status') #customer değilse vendor değil midir? ikisi için ayrı alanlara gerek var mı?
    contact_status_vendor = fields.Boolean(compute='_compute_contact_status')
    unknown_company = fields.Boolean(string="I don't know her/his company")
    type_of_material = fields.Many2many('type.material', string="Type of Material")

    #bu export, import ve customs_clearance fieldları yoktu ama xmlde kullanılıyor, hata verdiği için ben ekledim (doğa)
    export_operation = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Export Operation")
    export_operation_note = fields.Text(string="Export Operation Note")

    import_operation = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Import Operation")
    import_operation_note = fields.Text(string="Import Operation Note")

    customs_clearance = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Customs Clearance")
    customs_clearance_note = fields.Text(string="Customs Clearance Note")
    
    vendor_type = fields.Selection(
        [
            ('material', 'Material Supplier'),
            ('manufacturer', 'Manufacturer'),
            ('coating_supplier', 'Coating Supplier'),
            ('service', 'Service Provider'),
            ('certification', 'Certification/Licensing'),
            ], string="Vendor Type")

    is_customer = fields.Boolean(
        compute='_compute_contact_status_flags',
        store=False,  
    )
    is_vendor = fields.Boolean( #customer değilse vendor değil midir?
        compute='_compute_contact_status_flags',
        store=False,  
    )
    

    @api.onchange('type')
    def _onchange_type(self): #type değişirse bu fonk çalışır
        if self.type == 'driver':
            self.unknown_company = True
        else:
            self.unknown_company = False

    @api.depends('contact_status_vendor', 'contact_status_customer') #contact status yazıyordu sadece, hata alıyordum değiştirdim
    def _compute_contact_status_flags(self):
        for record in self:
            # 'Customer' veya 'Vendor' durumlarını kontrol et
            customer_status_names = record.contact_status.mapped('name')
            record.is_customer = 'Customer' in customer_status_names #if-else ile yapılabilir mi
            record.is_vendor = 'Vendor' in customer_status_names
            
    @api.depends('contact_status_customer', 'contact_status_vendor') #contact status yazıyordu sadece, hata alıyordum değiştirdim
    def _compute_contact_status(self):
        for record in self:
            status_names = record.contact_status.mapped('name')

            record.contact_status_customer = 'Customer' in status_names
            record.contact_status_vendor = 'Vendor' in status_names

    @api.constrains('phone', 'mobile', 'email')
    def _check_contact_info(self):
        for record in self:
            if record.type == 'driver':
                continue
            if not record.phone and not record.mobile and not record.email:
                raise ValidationError(_('You must fill at least one of the following: Phone, Mobile or Email!'))

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id.id == 224:
            self.lang = 'tr_TR'
        else:
            self.lang = 'en_US'
            
    def action_view_stock_moves(self):
        self.ensure_one()
       
        domain = [('customer', '=', self.id)]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'domain': domain,
            'context': {'default_customer': self.id},
        }