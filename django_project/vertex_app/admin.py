from django.contrib import admin

try:
    # For Django running
    from plugins.django_model_admin_custom_field_decorators.html import (
        a,
        img,
        separated_list
    )
except:
    # For PyCharm autocomplite only
    from django_project.plugins.django_model_admin_custom_field_decorators.html import (
        a,
        img,
        separated_list
    )
# Register your models here.

from . import models


class NoDeleteMixin:
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class NoAddMixin:
    def has_add_permission(self, request):
        return False


from django.urls import reverse
from django.http import HttpResponseRedirect


class NoEditMixin:
    list_display_links = None

    def change_view(self, request, object_id, extra_context=None):
        if object_id:
            extra_context = extra_context or {}
            extra_context['readonly'] = True
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False

        return super().change_view(request, object_id, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if hasattr(obj, 'pk') and obj.pk:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
        return self.readonly_fields


class ReadOnlyMixin(NoDeleteMixin, NoAddMixin, NoEditMixin):
    pass


class SubRequestStatusAdmin(ReadOnlyMixin, admin.ModelAdmin):
    fields = [
        'name',
        'code',
    ]
    list_display = (
        'id',
        'name',
        'code',
    )
    search_fields = [
        'name',
        'code',
    ]


admin.site.register(models.SubRequestStatus, SubRequestStatusAdmin)


class RequestAdmin(NoDeleteMixin, NoEditMixin, admin.ModelAdmin):
    readonly_fields = ('datetime',)
    fields = [
        'datetime',
        'content',
        'comment',
    ]
    list_display = (
        'id',
        'datetime',
        'get_sub_requests',
        'comment',
    )
    search_fields = [
        'content',
        'comment',
    ]

    @a(title='Перейти к подзапросам', text='use_orm__content')
    def get_sub_requests(self, obj):
        return '/vertex_app/subrequest/?request__id__exact=%s' % obj.pk




admin.site.register(models.Request, RequestAdmin)


class SubRequestAdmin(ReadOnlyMixin, admin.ModelAdmin):
    fields = [
        'request',
        'checker_name',
        'content',
        'status',
        'stopwatch',
        'result',
    ]
    list_display = (
        'request',
        'checker_name',
        'content',
        'status',
        'stopwatch',
        'result',
    )
    search_fields = [
        'status',
        'checker_name',
        'content',
        'result',
    ]


admin.site.register(models.SubRequest, SubRequestAdmin)
