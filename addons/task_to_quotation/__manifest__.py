{
    "name": "Task to Quotation",
    "version": "1.0",
    "summary": "Create quotations directly from tasks",
    "description": """
        This module allows creating sales quotations directly from project tasks.
        It adds a button to the task form view that generates a quotation based on task information.
    """,
    "category": "Sales/Project",
    "author": "Your Company",
    "website": "https://www.yourcompany.com",
    "depends": ["project", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}





