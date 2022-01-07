import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from census.models import Census
from store.models import Vote
from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id':vid})
            context['voting'] = json.dumps(r[0])

            if r[0]['end_date'] is None:
                stats = {}
                if(getEstadisticas('turnout', vid) != 0):
                    stats['census_size'] = getEstadisticas('census_size', vid)
                    stats['voters_turnout'] = getEstadisticas('turnout', vid)
                    stats['participation_ratio'] = round((stats['voters_turnout']/stats['census_size'])*100,2)
                
                    for i,j in stats.items():
                        context['stats_' + str(i)] = j
                else:
                    stats['census_size'] = 0
                    stats['voters_turnout'] = 0
                    stats['participation_ratio'] = 0
                            
                    for i,j in stats.items():
                        context['stats_' + str(i)] = j
        except Exception:
            raise Http404

        return context

def getEstadisticas(requerido, vid):
    if (requerido=="census_size"):
        return Census.objects.filter(voting_id=vid).count()
    elif (requerido=="turnout"):
        return Vote.objects.filter(voting_id=vid).count()
    else:
        return None


