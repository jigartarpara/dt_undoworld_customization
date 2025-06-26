# File path: your_custom_app/your_custom_app/report/iqc_report/iqc_report.py
import frappe
from frappe import _

def execute(filters=None):
    columns = [
        _("Item Name") + ":Link/Item:200",
        _("Received Qty") + ":Float:120",
        _("Pass") + ":Float:100",
        _("Fail") + ":Float:100",
        _("Fail %") + ":Percent:100",
        _("Pass %") + ":Percent:100"
    ]

    data = []
    
    results = frappe.db.sql("""
        SELECT 
            qi.item_code,
            SUM(qi.sample_size) AS received_qty,
            SUM(CASE WHEN qi.status = 'Accepted' THEN qi.sample_size ELSE 0 END) AS pass_qty,
            SUM(CASE WHEN qi.status = 'Rejected' THEN qi.sample_size ELSE 0 END) AS fail_qty
        FROM 
            `tabQuality Inspection` qi
        WHERE 
            qi.docstatus = 1
        GROUP BY 
            qi.item_code
    """, as_dict=True)

    for row in results:
        received = row.received_qty or 0
        passed = row.pass_qty or 0
        failed = row.fail_qty or 0
        fail_pct = (failed / received * 100) if received else 0
        pass_pct = (passed / received * 100) if received else 0

        data.append([
            row.item_code,
            received,
            passed,
            failed,
            fail_pct,
            pass_pct
        ])

    return columns, data
