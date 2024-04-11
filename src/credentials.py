import wsgiref.simple_server
from wsgiref import *
from loguru import logger
from urllib import parse


class Server:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 8888
        logger.info(f"Server inited on url: http://{self.ip}:{self.port}")
        self.data = {'Cyberman': 'John Lumic',
                     'Dalek': 'Davros',
                     'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
                     'Human': 'Leonardo da Vinci',
                     'Ood': 'Klineman Halpen',
                     'Silence': 'Tasha Lem',
                     'Slitheen': 'Coca-Cola salesman',
                     'Sontaran': 'General Staal',
                     'Time Lord': 'Rassilon',
                     'Weeping Angel': 'The Division Representative',
                     'Zygon': 'Broton'}

    def get_name(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/json; charset=utf-8')]
        response = {"credentials": "Unknown"}
        try:
            request = parse.parse_qs(environ['QUERY_STRING'])
            logger.info(f"Request income to program: {request}")
            if request and 'species' in request and request['species'][0] in self.data:
                response["credentials"] = self.data[request['species'][0]]
            else:
                logger.critical("Into program came uncorrected value")
        except Exception as ex:
            status = '500 BAD'
            logger.exception(f"{ex} spawned in function get_name")
        start_response(status, headers)
        logger.info(f"Send message is {response}")
        return [f"{response}".encode()]

    def start_server(self):
        with wsgiref.simple_server.make_server(self.ip, self.port, self.get_name) as httpd:
            logger.info(f"Server started on {self.ip}:{self.port}")
            httpd.serve_forever()


if __name__ == "__main__":
    server = Server()
    server.start_server()
