from abc import abstractmethod
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.http import Http404
from census.models import Census
from authentication.models import Persona
from .models import Vote
from .serializers import VoteSerializer
from base import mods
from base.perms import UserIsStaff
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render

class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id', 'voter_id')

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
        """

        vid = request.data.get('voting')
        voting = mods.get('voting', params={'id': vid})
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        end_date = voting[0].get('end_date', None)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        vote = request.data.get('vote')

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        token = request.auth.key
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = { "a": a, "b": b }
        v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,
                                          defaults=defs)
        v.a = a
        v.b = b

        v.save()

        return  Response({})

class PanelView(TemplateView):
    template_name='panel.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(not self.request.user.is_superuser):
            # return HttpResponse('Debe iniciar sesion como admin',status=403)
            context['message']='Debe iniciar sesion como admin'
            return context
        vid = kwargs.get('voting_id', 0)
        cens = Census.objects.filter(voting_id=vid)
        lista = []
        for i in cens:
            lista.append(User.objects.get(id=i.voter_id))
        personas = []
        for i in lista:
              personas.append(Persona.objects.get(usuario=i))#funcionara cuando se cree una nueva
    

        n_hombres = 0
        n_mujeres = 0
        n_otros = 0

        for p in personas:
            if p.sexo == "hombre" or p.sexo == "Hombre":
                n_hombres+=1
            elif p.sexo == "mujer" or p.sexo == "Mujer":
                n_mujeres+=1
            else:
                n_otros+=1

        menores = 0
        jovenes = 0
        veteranos = 0
        ancianos = 0

        for p in personas:
            if p.edad < 18:
                menores+=1
            elif p.edad>18 and p.edad<=30:
                jovenes+=1
            elif p.edad>30 and p.edad<=70:
                veteranos+=1
            elif p.edad>70:
                ancianos+=1

        pais_europa = ["AD","AL","AT","AX","BA","BE","BG","BY","CH","CZ","DK","DE","EE","ES","FI","FO","FR","GB","GG","GI","GR","HR","HU","IE","IM","IS","IT","JE","LI","LT","LU","LV","MC","MD","ME","MK","MT","NL","NO","PL","PT","RO","RS","RU","SE","SI","SJ","SK","SM","TR","UA","VA"]
        pais_asia = ["AE","AF","AM","AZ","BD","BH","BN","BT","CC","CN","CX","CY","GE","HK","ID","IL","IN","IO","IQ","IR","JO","JP","KG","KH","KP","KR","KW","KZ","LA","LB","LK","MM","MN","MO","MV","MY","NP","OM","PH","PK","PS","PS","QA","SA","SG","SY","TH","TJ","TL","TM","TW","UZ","VN","YE"]
        pais_africa = ["AO","BF","BI","BJ","BW","CD","CF","CG","CI","CM","CV","DJ","DZ","EG","EH","ER","ET","GA","GH","GM","GN","GQ","GW","KE","KM","LR","LS","LY","MA","MG","ML","MR","MU","MW","MZ","NA","NE","NG","RE","RW","SC","SD","SH","SL","SN","SO","SS","ST","SZ","TD","TG","TN","TZ","UG","YT","ZA","ZM","ZW"]
        pais_latam = ["AR","BO","BR","CL","CO","EC","FK","GF","GY","PE","PY","SR","UY","VE"]
        pais_norteAmerica = ["AG","AI","AW","BB","BL","BM","BQ","BS","BZ","CA","CR","CW","DM","DO","GD","GL","GP","GT","HN","HT","JM","KN","KY","LC","MF","MQ","MS","MX","NI","PA","PM","PR","SV","SX","TC","TT","US","VC","VG","VI"]

        europeos = 0
        africanos = 0
        asiaticos = 0
        latinoamericanos = 0
        norteamericanos = 0

        for p in personas:
            if p.region in pais_europa:
                europeos+=1
            elif p.region in pais_asia:
                asiaticos+=1
            elif p.region in pais_africa:
                africanos+=1
            elif p.region in pais_latam:
                latinoamericanos+=1
            elif p.region in pais_norteAmerica:
                norteamericanos+=1
        

        context['id']=vid
        context['vot']=lista
        context['pers']= personas
        
        context['n_hombres']=n_hombres
        context['n_mujeres']=n_mujeres
        context['n_otros']=n_otros

        context['menores']=menores
        context['jovenes']=jovenes
        context['veteranos']=veteranos
        context['ancianos']=ancianos

        context['europeos']=europeos 
        context['africanos']=africanos 
        context['asiaticos']=asiaticos 
        context['latinoamericanos']=latinoamericanos 
        context['norteamericanos']=norteamericanos 

        return context


# def crearSuperUser(request):
    
#     u = User.objects.get(username = 'administrador')
#     u.is_superuser = True
#     u.is_staff = True
#     u.save()

#     return render(request,'pruebita.html')
