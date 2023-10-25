# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Forecasts(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField(blank=True, null=True)
    short_question = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    resolution_criteria = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'forecasts'

class ForecastPoints(models.Model):
    update_id = models.AutoField(primary_key=True, blank=True, null=True)
    forecast = models.ForeignKey('Forecasts', on_delete=models.CASCADE, blank=True, null=True)
    point_forecast = models.FloatField(blank=True, null=True)
    upper_ci = models.FloatField(blank=True, null=True)
    lower_ci = models.FloatField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'forecast_points'

class Resolutions(models.Model):
    id = models.AutoField(primary_key=True)
    forecast = models.ForeignKey(Forecasts, on_delete=models.CASCADE, blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    resolution_date = models.DateTimeField(blank=True, null=True)
    brier_score = models.FloatField(blank=True, null=True)
    logn_score = models.FloatField(blank=True, null=True)
    log2_score = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'resolutions'
