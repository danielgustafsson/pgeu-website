from django import forms
from django.forms import ValidationError
from django.forms import widgets
from django.contrib.auth.models import User

from models import *

class InvoiceForm(forms.ModelForm):
	hidden_until_finalized = ('total_amount',)
	available_in_finalized = ('recipient_user', 'recipient_email', 'allowedmethods',)

	def __init__(self, *args, **kwargs):
		super(InvoiceForm, self).__init__(*args, **kwargs)
		# Some fields are hidden until the invoice is final
		if not self.instance.finalized:
			for fld in self.hidden_until_finalized:
				del self.fields[fld]

		self.fields['invoicedate'].widget = widgets.DateInput()
		self.fields['duedate'].widget = widgets.DateInput()
		self.fields['allowedmethods'].widget = forms.CheckboxSelectMultiple()
		self.fields['allowedmethods'].queryset = InvoicePaymentMethod.objects.all()
		self.fields['recipient_user'].queryset = User.objects.order_by('username')

		if self.instance.finalized:
			# All fields should be read-only for finalized invoices
			for fn,f in self.fields.items():
				if self.instance.ispaid or not fn in self.available_in_finalized:
					if type(f.widget).__name__ in ('TextInput', 'Textarea', 'DateInput'):
						f.widget.attrs['readonly'] = "readonly"
					else:
						f.widget.attrs['disabled'] = True

	class Meta:
		model = Invoice
		exclude = ['finalized', 'pdf_invoice', 'pdf_receipt', 'paidat', 'paymentdetails', 'processor', 'processorid', 'deleted']

	def clean(self):
		if not self.cleaned_data['recipient_user'] and self.cleaned_data['recipient_email']:
			# User not specified. If we can find one by email, auto-populate
			# the field.
			matches = User.objects.filter(email=self.cleaned_data['recipient_email'])
			if len(matches) == 1:
				self.cleaned_data['recipient_user'] = matches[0]
		return self.cleaned_data

class InvoiceRowForm(forms.ModelForm):
	class Meta:
		model = InvoiceRow

	def clean_rowamount(self):
		if self.cleaned_data['rowamount'] <= 0:
			raise ValidationError("Must specify an amount!")
		return self.cleaned_data['rowamount']
	def clean_rowcount(self):
		if self.cleaned_data['rowcount'] <= 0:
			raise ValidationError("Must specify a count!")
		return self.cleaned_data['rowcount']