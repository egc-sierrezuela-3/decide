from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from django import forms

from django.http import HttpResponse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
import csv
from census.forms import votacionForm
from rest_framework.permissions import IsAuthenticated

def CensusImport(request):
    
    if request.method == 'POST':
            try:
                nuevoCenso=request.FILES['nuevoCenso']
                votantes=[]
                votaciones=[]
                for row in nuevoCenso:
                    parse=str(row[:-1]).split(',')
                    votante=str(parse[0][2:])
                    votacion=str(parse[1][:-1])
                    votantes.append(votante)
                    votaciones.append(votacion)

                    try:
                        Census.objects.update_or_create(
                            voting_id=int(votacion),
                            voter_id=int(votante),
                        )
                    except:
                        return render(request,'censusImport.html',{'votantes':votantes,'votaciones':votaciones,'noimportado':'Ha habido un error'})
               
                return render(request,'censusImport.html',{'votantes':votantes,'votaciones':votaciones,'importado':'Los datos se han cargado correctamente'})

            except: 
               return render(request,'censusImport.html',{'vacio':'Selecciona un archivo csv con el formato indicado'})
    
    return render(request,'censusImport.html')


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})



class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')



def elegirVotacion(request):
    formulario = votacionForm()
    censos = None
    idVotacion = None
    if request.method == 'POST':
        formulario = votacionForm(request.POST)
        if formulario.is_valid(): #Corre la validación correspondiente
            idVotacion = formulario.cleaned_data['votacion']
            censos = Census.objects.filter(voting_id = idVotacion)
    return render(request, 'inicio.html', {'formulario':formulario, 'censos':censos, 'idVotacion':idVotacion})





def exportarCenso(request, idVotacion):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="censo.csv"'
    file = csv.writer(response)
    censos = Census.objects.filter(voting_id = idVotacion)
    file.writerow(['Id votante'])
    for c in censos:
        file.writerow([c.voter_id])

    return response
