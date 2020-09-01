class StatusCreator:
    """
    Create http status
    """

    class StatusIsNotExists(Exception):
        """
        Exception when status is not exists
        """

        def __init__(self, txt):
            self.txt = txt


    def __init__(self):
        self.info_status = {
            100: 'Continue',
            101: 'Switching Protocols',
            102: 'Processing',
        }
        self.success_status = {
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            207: 'Multi-Status',
            208: 'Already Reported',
            226: 'IM Used',
        }
        self.redirect_status = {
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            307: 'Temporary Redirect',
            308: 'Permanent Redirect',
        }
        self.client_error_status = {
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Payload Too Large',
            414: 'URI Too Long',
            415: 'Unsupported Media Type',
            416: 'Range Not Satisfiable',
            417: 'Expectation Failed',
            418: 'I’m a teapot',
            419: 'Authentication Timeout',
            421: 'Misdirected Request',
            422: 'Unprocessable Entity',
            423: 'Locked',
            424: 'Failed Dependency',
            426: 'Upgrade Required',
            428: 'Precondition Required',
            429: 'Too Many Requests',
            431: 'Request Header Fields Too Large',
            431: 'Requested host unavailable',
            449: 'Retry With',
            451: 'Unavailable For Legal Reasons',
            499: 'Client Closed Request',
        }
        self.server_error_status = {
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported',
            506: 'Variant Also Negotiates',
            507: 'Insufficient Storage',
            509: 'Bandwidth Limit Exceeded',
            510: 'Not Extended',
            511: 'Network Authentication Required',
            520: 'Unknown Error',
            521: 'Web Server Is Down',
            522: 'Connection Timed Out',
            523: 'Origin Is Unreachable',
            524: 'A Timeout Occurred',
            525: 'SSL Handshake Failed',
            526: 'Invalid SSL Certificate',
        }

    def __call__(self, number: int=200, status: str=None) -> str:
        """
        :param number: http status code
        :param status: http status info
        :return: code status
        """
        self.status_code = None

        if status is not None:
            self.status_code = f'{number} {status}'

        for status in (self.info_status, self.success_status, \
                self.redirect_status, self.client_error_status, \
                self.server_error_status):
            for code in status:
                if code == number:
                    self.status_code = f'{code} {status[code]}'

        if self.status_code is None:
            raise self.StatusIsNotExists('Status code is not exits, create yours http status')

        return self.status_code
