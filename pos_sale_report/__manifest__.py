{
    "name": "POS and Sales Reports",
    "version": "1.0",
    "category": "Productivity",
    "depends": ['base', 'sale_management', 'stock', 'purchase', 'point_of_sale', 'gift_card'],
    "description": "Reports for goods sold at price different from the fixed price, ",
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/res_config_settings_views.xml",
        "views/k_pos_wizard.xml",
        "views/k_pos_refund_wizard.xml",
        "views/k_sale_wizard.xml",
        "views/sales_price_difference.xml",
        "views/quantity_track.xml",
        "views/purchase_orders.xml",
        "views/k_pos_daily_reports.xml",
        "views/discounts.xml",
        "views/discounts_report.xml",
        "views/base-price.xml",
        "views/giftcards.xml",
        "views/refund_orders.xml",
        "views/scheduled_actions.xml",
        "reports/k_pos_refund_report.xml",
        "reports/k_pos_diff_report.xml",
        "reports/k_sale_diff_report.xml",
        "reports/quant_track_report.xml",
        "reports/sales_price_update-report.xml",
        "reports/purchase_order_report.xml",
        "reports/discounts_report.xml",
        "reports/product_discounts.xml",
        "reports/giftcards-reports.xml",
        "reports/refund_orders_report.xml",

    ],
    'license': 'LGPL-3',
}
