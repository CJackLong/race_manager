from django.contrib import admin

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



admin.site.register(Racer, RacerAdmin)
admin.site.register(Race)
admin.site.register(RacerResult)

