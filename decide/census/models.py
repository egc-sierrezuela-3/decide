from django.db import models
from census.validators import *

class Census(models.Model):
    voting_id = models.PositiveIntegerField(validators=[validation_census_voting_id])
    voter_id = models.PositiveIntegerField(validators=[validation_census_voter_id])


    class Meta:
        unique_together = (('voting_id', 'voter_id'),)
