import requests


class SPTransClient:

    def __init__(self, token):

        self.token = token

    """ A python client for the Olho Vivo API """

    session = requests.Session()
    url = 'http://api.olhovivo.sptrans.com.br/v2.1/'

    def auth(self):

        """
        In order to have access to the API service, we need to perform pre-use authentication using POST method. We
        inform our dev token and it returns true when the authentication succeeds.
        """

        method = 'Login/Autenticar?token=' + self.token
        response = self.session.post(self.url + method)

        if response.cookies:
            print('Connection established')
            return True

        return False

    def _get(self, path):

        """ Normal HTTP GET for all the other methods. """

        response = self.session.get(self.url + path)
        print(response.content)
        print(response.status_code)
        data = response.json()
        return data

    def search_by_busline(self, term):

        """
        Searches bus route by the name. If route is not found, a phonetic seach is performed.
        """

        return self._get('Linha/Buscar?termosBusca=%s' % term)

    def get_bus_detail(self, uid):

        """
        Gets bus detail from a certain bus route if you provide a uid or from all bus routes if you don't.
        """

        return self._get('Linha/CarregarDetalhes?codigoLinha=%s' % uid)

    def search_by_stops(self, term):

        """
        Phonetic search of the stop name or of the stop address.
        """

        return self._get('Parada/Buscar?termosBusca=%s' % term)

    def search_stops_by_bus(self, uid):

        """
        Realiza uma busca por todos os pontos de parada atendidos por
        uma determinada linha.
        """

        return self._get('Parada/BuscarParadasPorLinha?codigoLinha=%s' % uid)

    def get_bus_position(self, uid):

        """
        Gets all bus positions from a certain bus line.
        """

        return self._get('Posicao?codigoLinha=%s' % uid)

    def get_all_bus_positions(self):
        
        """
        Gets all bus positions.
        """

        return self._get('Posicao')

    def get_next_bus(self, stop_id, bus_id):

        """
        Gets the expected time of the next bus getting to a all of the lines bus stops.
        """

        return self._get('Previsao?codigoParada=%s&codigoLinha=%s' % (stop_id,
                                                                      bus_id))

    def get_next_bus_in_stop(self, stop_id):

        """
        Gets the expected time to the buses of all lines to get to a certain stop.
        """

        return self._get('Previsao/Parada?codigoParada=%s' % stop_id)