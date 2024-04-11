import logging
from functools import wraps
import argparse
from time import perf_counter
from loguru import logger
import requests
import bs4


def Loger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        logger.info(f"function start: ({func.__name__}) with parameters: {args} :\n")
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            logger.info(f"The function ({func.__name__}) ended with the result: {result}")
            logger.info(f"The function ({func.__name__}) has been completed for {(perf_counter() - start):.4f}\n")
        except Exception:
            logger.exception(f"the function ({func.__name__}) ended with an error\n")
        return result

    return wrapper


@Loger
def Upload(filepath):
    files = {'file': open(filepath, 'rb')}
    response = requests.post("http://localhost:8888/", files=files)
    if response.status_code == 200:
        print('File uploaded successfully')
    else:
        print('Failed to upload file', response.status_code)


@Loger
def GetList():
    response = requests.get("http://localhost:8888/")
    if response.status_code == 200:
        print('List of files on the server:')
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                print(cells[0].text.strip())
    else:
        print('Failed to retrieve file list')


@Loger
def InitArgs(parser):
    parser.add_argument('upload', nargs=1, type=str,
                        help="""Command for upload into server the audio file, return value is server response status 
                        code""",
                        default=None)
    parser.add_argument('list', nargs='?', default=None, help="""Command for get from server list of all music on 
    server""")
    return parser.parse_args()


@Loger
def main():
    parser = argparse.ArgumentParser()
    args = InitArgs(parser)
    if args.upload[0] == 'upload' and args.list is not None:
        logger.info(f"Status code: {Upload(args.list)}")
    elif args.upload[0] == 'list' and args.list is None:
        GetList()
    else:
        logging.error("Bad value gived")


if __name__ == "__main__":
    main()
