from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return out

    def borda(self, options):
        out = []
        #Numero total de questions para ordenar por preferencia
        n = len(options)

        for opt in options:
            votos = 0
            preference = 0

            while preference < n:
                #Preference es una variable que indica el orden de preferencia de las respuestas a las questions de las votaciones
                votos += (n-preference)* opt['votes'][preference]
                preference +=1

            out.append({
                    **opt,
                    'postproc': votos,
                })

        out.sort(key=lambda x: -x['postproc'])
        return out

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        out = []
        questions = request.data

        for q in questions:
            result = None
            t = q['type']
            opts = q['options']

            if t == 'IDENTITY':
                result = self.identity(opts)
            '''if t == 'BORDA':
                result = self.borda(opts)
            if t == 'EQUALITY':
                result = self.equality(opts)
            if t == 'SAINTE_LAGUE' or t == 'HONDT':
                result = self.proportional_representation(opts, t)
            if t == 'DROOP':
                result = self.droop(opts)
            if t == 'IMPERIALI':
                result = self.imperiali(opts)
            if t == 'HARE':
                result = self.hare(opts)'''

            out.append({'type': t, 'options': result})


        return Response(out)
