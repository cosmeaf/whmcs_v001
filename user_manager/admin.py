from django.contrib import admin
from .models import Member, Domain
from django.utils.html import format_html

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'uid', 'gid', 'home_directory', 'shell', 'sudo_access')
    search_fields = ('username', 'user__username', 'uid', 'gid')
    list_filter = ('sudo_access', 'shell')
    ordering = ('username',)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('member', 'subdomain', 'requests', 'visitors', 'files_count', 'data_usage_kb', 'subdomain_url')
    search_fields = ('subdomain', 'member__username')
    ordering = ('subdomain',)

    def subdomain_url(self, obj):
        return format_html(
            '<a href="https://{}.{}" target="_blank">{}</a>',
            obj.subdomain,
            'projetodesenvolve.site',  # Troque por seu domínio
            f'https://{obj.subdomain}.projetodesenvolve.site'
        )
    subdomain_url.short_description = 'Subdomain URL'
