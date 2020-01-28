from django.contrib import admin

from . models import PrintRequest, PrintRequestFile

@admin.register(PrintRequest)
class PrintRequestAdmin(admin.ModelAdmin):

    list_display = ('id', '__str__', 'status', 'amount', 'printed_on', 'cancelled_on', 'paid_on', 'is_deleted')
    list_display_links = ('__str__',)
    list_filter = ('is_color', 'status', 'is_deleted')
    list_per_page = 100
    search_fields = ('client',)
    empty_value_display = 'NULL'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'amount')

    actions = ['soft_delete', 'remove_soft_delete']

    def soft_delete(self, request, queryset):
        rows_updated = queryset.update(is_deleted=True)
        if rows_updated == 1:
            message_bit = "1 print request was"
        else:
            message_bit = "%s print requests were" % rows_updated
        self.message_user(request, "%s successfully marked as Soft deleted." % message_bit)
    soft_delete.short_description = "Soft delete selected books"

    def remove_soft_delete(self, request, queryset):
        rows_updated = queryset.update(is_deleted=False)
        if rows_updated == 1:
            message_bit = "1 print request was"
        else:
            message_bit = "%s print requests were" % rows_updated
        self.message_user(request, "%s successfully removed as Soft deleted." % message_bit)
    remove_soft_delete.short_description = "Remove soft delete from selected books"

    class Meta:
        model = PrintRequest

@admin.register(PrintRequestFile)
class PrintRequestFileAdmin(admin.ModelAdmin):

    list_display = ('id', '__str__', 'no_of_copies', 'is_deleted')
    list_display_links = ('__str__',)
    list_filter = ('is_deleted', )
    list_per_page = 100
    empty_value_display = 'NULL'
    ordering = ('-created_at',)
    readonly_fields = ("created_at", "updated_at")

    actions = ['soft_delete', 'remove_soft_delete']

    def soft_delete(self, request, queryset):
        rows_updated = queryset.update(is_deleted=True)
        if rows_updated == 1:
            message_bit = "1 book was"
        else:
            message_bit = "%s books were" % rows_updated
        self.message_user(request, "%s successfully marked as Soft deleted." % message_bit)
    soft_delete.short_description = "Soft delete selected books"

    def remove_soft_delete(self, request, queryset):
        rows_updated = queryset.update(is_deleted=False)
        if rows_updated == 1:
            message_bit = "1 book was"
        else:
            message_bit = "%s books were" % rows_updated
        self.message_user(request, "%s successfully removed as Soft deleted." % message_bit)
    remove_soft_delete.short_description = "Remove soft delete from selected books"

    class Meta:
        model = PrintRequestFile
