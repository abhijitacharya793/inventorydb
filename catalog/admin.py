from django.contrib import admin

# Register your models here.
from catalog.models import Manufacturer, Itemtype, Item, ItemInstance

#admin.site.register(Item)
#admin.site.register(Manufacturer)
admin.site.register(Itemtype)
#admin.site.register(ItemInstance)

class ItemsInline(admin.TabularInline):
    model = Item

# Define the admin class
class ManufacturerAdmin(admin.ModelAdmin):
        list_display = ('company_name', 'address')
        inlines = [ItemsInline]

# Register the admin class with the associated model
admin.site.register(Manufacturer, ManufacturerAdmin)

class ItemsInstanceInline(admin.TabularInline):
    model = ItemInstance

# Register the Admin classes for Book using the decorator
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'manufacturer')
    inlines = [ItemsInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(ItemInstance)
class ItemInstanceAdmin(admin.ModelAdmin):
    list_display = ('item', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('item', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
