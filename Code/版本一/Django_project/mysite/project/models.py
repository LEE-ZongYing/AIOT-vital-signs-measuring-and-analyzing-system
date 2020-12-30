from django.db import models
class Iccard(models.Model):
    name = models.CharField(max_length=45)
    id_card = models.CharField(max_length=45)
    cardnum = models.CharField(max_length=45)
    birthday = models.CharField(max_length=45)
    sex = models.CharField(max_length=45)
    carddate = models.CharField(max_length=45)
    temperature = models.CharField(max_length=45)
    weight = models.CharField(max_length=45)
    pressures = models.CharField(db_column='pressureS', max_length=45)  # Field name made lowercase.
    pressured = models.CharField(db_column='pressureD', max_length=45)  # Field name made lowercase.
    testdate = models.CharField(max_length=45)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iccard'
  
# Create your models here.
