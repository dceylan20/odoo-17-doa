from odoo import models, fields

class Supplier(models.Model):
    _inherit = 'res.partner'  # extending contact module

    industry_ids = fields.Many2many('industry', string='Industry')
    material_ids = fields.Many2many('material', string='Materials')
    certification_ids = fields.Many2many('certification', string='Certifications')
    quality_control_ids = fields.Many2many('quality.control', string='Quality Control')
    language_ids = fields.Many2many('language', string='Languages')
    production_method_ids = fields.Many2many('production.method', string='Production Methods')
    production_method_feature_ids = fields.Many2many('production.method.feature', string='Production Method Features')
    approved_method_ids = fields.Many2many('approved.method', string='Approved Production Methods')
    extra_info = fields.Char(string='Extra Information')

    def action_open_edit(self):
            return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Wizard',
            'res_model': 'edit.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('contact_onboarding.view_supplier_classification_wizard').id,
            'target': 'new',
            'context': {'default_name': 'Default Name'}
        }

        
class Industry(models.Model): 
    _name = 'industry'
    _description = 'Industry'

    name = fields.Char(string='Name', required=True, store=True)  #color değişmiyor, hep kırmızı kalıyor, düzeltilecek
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class Material(models.Model):
    _name = 'material'
    _description = 'Materials'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class Certification(models.Model):
    _name = 'certification'
    _description = 'Certifications'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class QualityControl(models.Model):
    _name = 'quality.control'
    _description = 'Quality Control'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class Language(models.Model):
    _name = 'language'
    _description = 'Language'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class ProductionMethods(models.Model):
    _name = 'production.method'
    _description = 'Production Methods'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class ProductionMethodFeatures(models.Model):
    _name = 'production.method.feature'
    _description = 'Production Method Features'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    )

class ApprovedProductionMethod(models.Model):
    
    _name = 'approved.method'
    _description = 'Approved Production Methods'

    name = fields.Char(string='Name', required=True)
    color = fields.Selection(
        [('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow')],
        string='Color',
        default='red'
    ) 


