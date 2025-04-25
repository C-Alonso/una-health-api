from django.contrib import admin
from .models import GlucoseReading

# Register your models here.
class GlucoseReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'glucose_level', 'reading_datetime')
    search_fields = ('user__username', 'user__email')
    list_filter = ('reading_datetime',)
    ordering = ('-reading_datetime',)

admin.site.register(GlucoseReading, GlucoseReadingAdmin)
