from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from voting.models import Voting

def validation_census_voting_id(value):
    votings_exitentes=Voting.objects.all()
    ids=[]
    for i in range(0,len(votings_exitentes)):
        ids.append(int(votings_exitentes[i].id))
    if value not in ids:
        raise ValidationError('La votación no existe')

def validation_census_voter_id(value):
    voters_exitentes=User.objects.all()
    ids=[]
    for i in range(0,len(voters_exitentes)):
        ids.append(int(voters_exitentes[i].id))
    if value not in ids:
        raise ValidationError('El/La votante no existe')
