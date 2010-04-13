from django.contrib import admin
from models import *

class TransactionInfoAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'sourceaccount', 'sender', 'amount', 'transtext', 'matched', )
	list_filter = ('sourceaccount', 'matched', )
	ordering = ('-timestamp', )

class ErrorLogAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'sent', 'message', )
	list_filter = ('sent', )
	ordering = ('-timestamp', )

admin.site.register(SourceAccount)
admin.site.register(TransactionInfo, TransactionInfoAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)