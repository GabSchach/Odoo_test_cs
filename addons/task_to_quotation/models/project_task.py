from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    # Add fields to store available products for quotation (optional)
    quotation_product_ids = fields.Many2many(
        'product.product', 
        string='Products for Quotation',
        help='Products that will be included in the quotation created from this task'
    )
    





    # Add method to create quotation
    def action_create_quotation(self):
        self.ensure_one()
        
        # Check if customer is set
        if not self.partner_id:
            raise UserError(_("Please set a customer for this task before creating a quotation."))
        
        # Prepare quotation values
        sale_order_vals = {
            'partner_id': self.partner_id.id,
            'origin': self.name,
        }
        
        # Create quotation
        sale_order = self.env['sale.order'].create(sale_order_vals)
        
        # Add products to quotation
        if self.quotation_product_ids:
            for product in self.quotation_product_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': 1.0,
                })
        else:
            # If no products are specified, add a service product
            # Create a line based on task name
            product = self.env['product.product'].search([('name', '=', 'Task Service')], limit=1)
            if not product:
                # Create a default service product if it doesn't exist
                product = self.env['product.product'].create({
                    'name': 'Task Service',
                    'type': 'service',
                    'invoice_policy': 'order',
                    'sale_ok': True,
                })
            
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': self.name,
                'product_uom_qty': 1.0,
            })
        
        # Parse the description field to extract dataset information
        description = self.description or ""
        if "Dataset" in description:
            # This is a very basic implementation - you would need more sophisticated
            # parsing based on your actual data structure
            dataset_products = self.env['product.product'].search([('name', 'ilike', 'Dataset')])
            for product in dataset_products:
                if product.name in description:
                    self.env['sale.order.line'].create({
                        'order_id': sale_order.id,
                        'product_id': product.id,
                        'product_uom_qty': 1.0,
                    })
        
        # Link the task to the quotation (if you have a field for this)
        # self.sale_order_id = sale_order.id
        
        # Return action to view the created quotation
        return {
            'name': _('Quotation'),
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'type': 'ir.actions.act_window',
        }