"""contact/admin.py"""

from django.contrib import admin
from contact.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('status',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip_address', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        # Messages are only created via the contact form
        return False
