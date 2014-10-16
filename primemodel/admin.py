from django.contrib import admin

from primemodel.models import *

class PopulationAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'owner', 'created_at', 'updated_at')

class PopulationSubsetAdmin(admin.ModelAdmin):
	list_display = ('id', 'population', 'age_group', 'gender', 'size', 'created_at', 'updated_at')

class OutcomeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'outcomegroup', 'shortname', 'icd10_name', 'icd10_code', 'created_at', 'updated_at')

class OutcomeGroupAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'code', 'shortname')

class MortalityAdmin(admin.ModelAdmin):
	list_display = ('id', 'population_subset', 'outcome', 'value', 'owner', 'created_at', 'updated_at')

class ExposureGroupAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')

class ExposureAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'exposure_group', 'created_at', 'updated_at')

class ExposureDistributionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'distribution_type', 'randomised_estimate', 'ci_low', 'ci_high', 'sd', 'mean', 'original_estimate', 'lower_estimate_limit', 'upper_estimate_limit', 'reference')

class MeasurementAdmin(admin.ModelAdmin):
	list_display = ('id', 'measurement_type', 'population_subset', 'measurement_option', 'value', 'owner', 'created_at', 'updated_at')

class MeasurementTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'exposure', 'unit', 'created_at', 'updated_at')

class ReferenceAdmin(admin.ModelAdmin):
	list_display = ('id', 'meta_analysis_ref', 'shortname', 'title', 'authors', 'journal_name', 'volume_number', 'year_published', 'page_numbers', 'created_at', 'updated_at')

class RelativeRiskAdmin(admin.ModelAdmin):
	list_display = ('id', 'exposure', 'outcome', 'bin_value', 'exposure_distribution', 'population_subset', 'created_at', 'updated_at')

class ExposureBinsAdmin(admin.ModelAdmin):
	list_display = ('id', 'exposure', 'bin_type', 'bin_value')

admin.site.register(Population, PopulationAdmin)
admin.site.register(PopulationSubset, PopulationSubsetAdmin)
admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(OutcomeGroup, OutcomeGroupAdmin)
admin.site.register(Mortality, MortalityAdmin)
admin.site.register(ExposureGroup, ExposureGroupAdmin)
admin.site.register(Exposure, ExposureAdmin)
admin.site.register(ExposureDistribution, ExposureDistributionAdmin)
admin.site.register(MeasurementType, MeasurementTypeAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(RelativeRisk, RelativeRiskAdmin)
admin.site.register(ExposureBins, ExposureBinsAdmin)
