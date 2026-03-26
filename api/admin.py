from django.contrib import admin, messages

from .models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "last_used_at", "created_at")
    list_filter = ("is_active",)
    readonly_fields = ("guid", "key_hash", "last_used_at", "created_at", "updated_at")
    fields = ("name", "scopes", "is_active", "guid", "key_hash", "last_used_at", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not change:
            api_key, raw_key = ApiKey.generate(name=obj.name, scopes=obj.scopes or ["*"])
            messages.info(request, f"API Key (copy now, shown once): {raw_key}")
            # Don't call super — generate() already saved
            return
        super().save_model(request, obj, form, change)
