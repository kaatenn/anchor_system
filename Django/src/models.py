# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnchorAcPass(models.Model):
    account = models.CharField(primary_key=True, max_length=10)
    password = models.CharField(max_length=18)

    class Meta:
        db_table = 'anchor_ac_pass'


class AnchorInfo(models.Model):
    account = models.OneToOneField(AnchorAcPass, models.DO_NOTHING, db_column='account', primary_key=True)
    nickname = models.CharField(db_column='nickName', max_length=10)  # Field name made lowercase.
    sex = models.IntegerField()
    telephone_number = models.CharField(max_length=11, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'anchor_info'


class ChairmanAcPass(models.Model):
    account = models.CharField(primary_key=True, max_length=10)
    password = models.CharField(max_length=18)

    class Meta:
        db_table = 'chairman_ac_pass'


class ChairmanInfo(models.Model):
    nickname = models.CharField(db_column='nickName', max_length=10)  # Field name made lowercase.
    account = models.OneToOneField(ChairmanAcPass, models.DO_NOTHING, db_column='account', primary_key=True)
    sex = models.IntegerField()
    telephone_number = models.CharField(max_length=11, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    is_waiting = models.IntegerField()

    class Meta:
        db_table = 'chairman_info'


class Employment(models.Model):
    administer = models.OneToOneField(ChairmanAcPass, models.DO_NOTHING, db_column='administer', primary_key=True)
    anchor = models.ForeignKey(AnchorAcPass, models.DO_NOTHING, db_column='anchor')
    goaltime = models.IntegerField()
    salary = models.IntegerField()
    workingstatus = models.IntegerField()
    worktime = models.IntegerField()
    start_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'employment'
        unique_together = (('administer', 'anchor'),)


class Wanting(models.Model):
    anchor = models.OneToOneField(AnchorAcPass, models.DO_NOTHING, db_column='anchor', primary_key=True)
    administer = models.ForeignKey(ChairmanAcPass, models.DO_NOTHING, db_column='administer')
    wanted_salary = models.IntegerField()
    wanted_salary_fluctuation = models.IntegerField(blank=True, null=True)
    wanted_goal_time = models.IntegerField()
    wanted_goal_time_fluctuation = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'wanting'
        unique_together = (('anchor', 'administer'),)
