from odoo import models, fields, api

class EditWizard(models.Model):
    _name = 'edit.wizard'
    _description = 'Edit Wizard'

    industry_ids = fields.Many2many('industry', string='Industry')
    material_ids = fields.Many2many('material', string='Materials')
    certification_ids = fields.Many2many('certification', string='Certifications')
    quality_control_ids = fields.Many2many('quality.control', string='Quality Control')
    language_ids = fields.Many2many('language', string='Languages')
    production_method_ids = fields.Many2many('production.method', string='Production Methods')
    production_method_feature_ids = fields.Many2many('production.method.feature', string='Production Method Features')
    approved_method_ids = fields.Many2many('approved.method', string='Approved Production Methods')
    extra_info = fields.Char(string='Extra Information')

    def apply_changes(self):
        active_id = self.env.context.get('active_id')
        partner = self.env['res.partner'].browse(active_id)
        partner.industry_ids = [(6, 0, self.industry_ids.ids)]
        partner.material_ids = [(6, 0, self.material_ids.ids)]
        partner.certification_ids = [(6, 0, self.certification_ids.ids)]
        partner.quality_control_ids = [(6, 0, self.quality_control_ids.ids)]
        partner.language_ids = [(6, 0, self.language_ids.ids)]
        partner.production_method_ids = [(6, 0, self.production_method_ids.ids)]
        partner.production_method_feature_ids = [(6, 0, self.production_method_feature_ids.ids)]
        partner.approved_method_ids = [(6, 0, self.approved_method_ids.ids)]
        partner.extra_info = self.extra_info

    @api.model
    def default_get(self, fields):
        res = super(EditWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        partner = self.env['res.partner'].browse(active_id)

        res['industry_ids'] = partner.industry_ids.ids
        res['material_ids'] = partner.material_ids.ids
        res['certification_ids'] = partner.certification_ids.ids
        res['quality_control_ids'] = partner.quality_control_ids.ids
        res['language_ids'] = partner.language_ids.ids
        res['production_method_ids'] = partner.production_method_ids.ids
        res['production_method_feature_ids'] = partner.production_method_feature_ids.ids
        res['approved_method_ids'] = partner.approved_method_ids.ids
        res['extra_info'] = partner.extra_info

        return res

