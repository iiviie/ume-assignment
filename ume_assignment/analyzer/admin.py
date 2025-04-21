from django.contrib import admin
from .models import QueryLog

@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'query_preview', 'tone', 'intent')
    search_fields = ('query', 'tone', 'intent')
    list_filter = ('tone', 'intent', 'timestamp')

    def query_preview(self, obj):
        return obj.query[:50]
    query_preview.short_description = 'Query Preview'


