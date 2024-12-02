from django.contrib import admin
from .models import Image
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created')
    #search_fields = ('id',)
    list_filter = ('created',)
    #ordering = ('-uploaded_at',)
