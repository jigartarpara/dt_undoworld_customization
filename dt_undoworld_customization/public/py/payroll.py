import json
import frappe
import erpnext
from frappe import _
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry

class customPayrollEntry(PayrollEntry):
    def make_accrual_jv_entry(self, submitted_salary_slips):
        self.check_permission("write")
        
        # Convert end_date to datetime.date object if it is a string
        if isinstance(self.end_date, str):
            self.end_date = frappe.utils.getdate(self.end_date)

        # Check if end_date is before July 31, 2024
        cutoff_date = frappe.utils.getdate("2024-07-31")
        if self.end_date <= cutoff_date:
            frappe.msgprint(_("Journal Voucher will not be created as the end date is before July 31, 2024"), alert=True, indicator="red")
            return

        employee_wise_accounting_enabled = frappe.db.get_single_value(
            "Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
        )
        self.employee_based_payroll_payable_entries = {}
        self._advance_deduction_entries = []

        earnings = (
            self.get_salary_component_total(
                component_type="earnings",
                employee_wise_accounting_enabled=employee_wise_accounting_enabled,
            )
            or {}
        )

        deductions = (
            self.get_salary_component_total(
                component_type="deductions",
                employee_wise_accounting_enabled=employee_wise_accounting_enabled,
            )
            or {}
        )

        precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

        if earnings or deductions:
            accounts = []
            currencies = []
            payable_amount = 0
            accounting_dimensions = get_accounting_dimensions() or []
            company_currency = erpnext.get_company_currency(self.company)

            payable_amount = self.get_payable_amount_for_earnings_and_deductions(
                accounts,
                earnings,
                deductions,
                currencies,
                company_currency,
                accounting_dimensions,
                precision,
                payable_amount,
            )

            payable_amount = self.set_accounting_entries_for_advance_deductions(
                accounts,
                currencies,
                company_currency,
                accounting_dimensions,
                precision,
                payable_amount,
            )

            self.set_payable_amount_against_payroll_payable_account(
                accounts,
                currencies,
                company_currency,
                accounting_dimensions,
                precision,
                payable_amount,
                self.payroll_payable_account,
                employee_wise_accounting_enabled,
            )

            self.make_journal_entry(
                accounts,
                currencies,
                self.payroll_payable_account,
                voucher_type="Journal Entry",
                user_remark=_("Accrual Journal Entry for salaries from {0} to {1}").format(
                    self.start_date, self.end_date
                ),
                submit_journal_entry=True,
                submitted_salary_slips=submitted_salary_slips,
            )
