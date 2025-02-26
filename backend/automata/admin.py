from django.contrib import admin
from .models import AutomataModel

@admin.register(AutomataModel)
class AutomataModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'automata_type', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('automata_type', 'created_at')