from django.contrib import admin
from django.shortcuts import render,render_to_response
from .models import Census
from django.http import HttpResponse
from . import views
from django.contrib import messages
import csv
from django.contrib.auth.models import User


class SexCensusFilter(admin.SimpleListFilter):
    title = "Filtro por sexo"  # a label for our filter
    parameter_name = 'sexo'

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("hombre", "Hombre"),
            ("mujer", "Mujer"),
            ("otro", "Otro")
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == "hombre":
            # Para cada censo, busco el user y veo su género. Si el género es masculino
            # entonces añado el c.voting_id en una lista, y después retorno 
            # aquellos objetos mediante el filtro voter_id__in = lista
            lista_censos_hombres = []
            for c in queryset:
                usuario = User.objects.get(id=c.voter_id)
                persona = usuario.persona
                if persona.sexo == "hombre":
                    lista_censos_hombres.append(c.voter_id)
            return queryset.filter(voter_id__in=lista_censos_hombres)

        if self.value() == "mujer":
            lista_censos_mujeres = []
            for c in queryset:
                usuario = User.objects.get(id=c.voter_id)
                persona = usuario.persona
                if persona.sexo == "mujer":
                    lista_censos_mujeres.append(c.voter_id)
            return queryset.filter(voter_id__in=lista_censos_mujeres)

        if self.value() == "otro":
            lista_censos_otro = []
            for c in queryset:
                usuario = User.objects.get(id=c.voter_id)
                persona = usuario.persona
                if persona.sexo == "otro":
                    lista_censos_otro.append(c.voter_id)
            return queryset.filter(voter_id__in=lista_censos_otro)


class AgeCensusFilter(admin.SimpleListFilter):
    title = "Filtro por edad"  # a label for our filter
    parameter_name = 'edad'

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("18-30", "18 a 30 años"),
            ("31-50", "31 a 50 años"),
            ("50+", "Más de 50 años")
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == "18-30":
            # Para cada censo, busco el user y veo su edad. Si la edad está comprendida en el rango
            # entonces añado el c.voter_id en una lista, y después retorno 
            # aquellos objetos mediante el filtro voter_id__in = lista
            lista_censos = []
            for c in queryset:
                usuario = User.objects.get(id=c.voter_id)
                persona = usuario.persona
                if persona.edad >= 18 and persona.edad <= 30:
                    lista_censos.append(c.voter_id)
            print(lista_censos)
            return queryset.filter(voter_id__in=lista_censos)

        if self.value() == "31-50":
            lista_censos = []
            for c in queryset:
                usuario = User.objects.get(id=c.voter_id)
                print(usuario)
                persona = usuario.persona
                if persona.edad >= 31 and persona.edad <= 50:
                    lista_censos.append(c.voter_id)
            return queryset.filter(voter_id__in=lista_censos)
        
        if self.value() == "50+":
            lista_censos = []
            for c in queryset:
                usuario = User.objects.get(id=c.voter_id)
                print(usuario)
                persona = usuario.persona
                if persona.edad >50:
                    lista_censos.append(c.voter_id)
            return queryset.filter(voter_id__in=lista_censos)



class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', SexCensusFilter, AgeCensusFilter)

    search_fields = ('voter_id',)

    actions = ['import_census','export_census']

    def export_census(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="censo.csv"'
        file = csv.writer(response)
        file.writerow(['Id votante', 'Id votación'])
        ids = []
        for c in queryset:
            #if c.voter_id not in ids:
                file.writerow([c.voter_id, c.voting_id])
                ids.append(c.voter_id)

        self.message_user(request, "Exportación realizada con éxito", level=messages.SUCCESS)

        return response

    def import_census(self,request,queryset):
        return render(request,'censusImport.html')


admin.site.register(Census, CensusAdmin)

