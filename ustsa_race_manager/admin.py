from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Racer, Race, RacerResult

class RaceResultInline(admin.TabularInline):
    model = RacerResult
    extra = 1

class RacerAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields':
                    [
                        'first_name',
                        'last_name',
                        'ustsa_num',
                        'inj',
                        'racer_gender',

                    ]
            }
        )
    ]
    inlines = [RaceResultInline]

class RaceResource(resources.ModelResource):

    class Meta:
        model = Race


class RaceAdmin(ImportExportModelAdmin):
    resource_class = RaceResource
    inlines = [RaceResultInline]

admin.site.register(Racer, RacerAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(RacerResult)

