from django.contrib import admin
from django import forms
from import_export import resources
from import_export.fields import Field
from import_export.forms import ImportForm, ConfirmImportForm
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin, ImportMixin
import json
# Register your models here.
from .models import Racer, Race, RacerResult, Assignments, RaceOfficial, PublishedPointsList, RacerPoints


class CustomImportForm(ImportForm):
    race = forms.ModelChoiceField(
        queryset=Race.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    race = forms.ModelChoiceField(
        queryset=Race.objects.all(),
        required=True)


class RacerPointsInline(admin.TabularInline):
    model = RacerPoints
    extra = 1


class RaceResultInline(admin.TabularInline):
    model = RacerResult
    extra = 1


class RaceOfficialInline(admin.TabularInline):
    model = Assignments
    extra = 1


class RacerPointsResource(resources.ModelResource):
    class Meta:
        model = RacerPoints


class RacerResource(resources.ModelResource):
    class Meta:
        model = Racer


class ResultsResource(resources.ModelResource):
    racer = Field(
        column_name='ustsa_num',
        attribute='ustsa_num',
        widget=ForeignKeyWidget(Racer, 'ustsa_num')
    )

    class Meta:
        model = RacerResult

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        try:
            Race.objects.get(id = dataset['race'][1])
        except:
            print("the race doesn't exist")

    def after_import(self,dataset, result, using_transactions, dry_run, **kwargs):
        race = Race.objects.get(id = dataset['race'][1])
        Race.race_points.set_race_points(race.id)
        Race.race_points.calculate_race_penalty(race.id)


class RacerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = RacerResource

    fieldsets = [
        (None, {
            'fields': [
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


class RacerResultAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ResultsResource

    def get_import_form(self):
        return CustomImportForm

    def get_confirm_import_form(self):
        return CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        # pass on `race` to the kwargs for the custom confirm form
        print("was Called", form)

        if isinstance(form, CustomImportForm):
            if form.is_valid():
                race = form.cleaned_data['race']
                kwargs.update({'race': race.id})
        return kwargs


class RaceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [RaceResultInline, RaceOfficialInline]

    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status='p')

    make_published.short_description = "Mark races as ready to be published"

class RacerPointsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = RacerPointsResource





admin.site.register(Racer, RacerAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(RacerResult, RacerResultAdmin)
admin.site.register(RaceOfficial)
admin.site.register(RacerPoints, RacerPointsAdmin)
admin.site.register(PublishedPointsList)



