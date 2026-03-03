{
    "name": "Repair Workorder Community V2",
    "version": "16.0.1.0",
    "author": "Paulo Moretto",
    "category": "Manufacturing",
    "depends": [
        "repair",
        "mrp",
        "hr"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/repair_order_views.xml",
        "views/repair_workorder_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "repair_workorder_community_v2/static/src/js/repair_timer.js"
        ]
    },
    "installable": True,
}
