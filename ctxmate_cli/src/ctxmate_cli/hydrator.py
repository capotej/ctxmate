from urllib.parse import urlparse, ParseResult

import requests

def handle_web(pr: ParseResult) -> str:
    r = requests.get(pr.geturl(), allow_redirects=True)
    if r.ok:
        return str(r.content)
    else:
        return pr.path # this contains the unparsed string


def handle_file(pr: ParseResult) -> str:
    try:
        # Account for differences in how file paths are represented
        # on different operating systems.  Windows, for example, may have
        # a leading slash after the drive letter.
        file_path = pr.path
        if pr.netloc:  # Handle UNC paths (e.g., file://server/share/file.txt)
            file_path = '//' + pr.netloc + file_path
        elif file_path.startswith('///'): #for windows
            file_path = file_path[2:]
        elif file_path.startswith('//'):
            file_path = file_path[1:]

        with open(file_path, 'r') as f:
            file_content = f.read()
        return file_content
    except FileNotFoundError:
        return ""
    except Exception as e:
        return ""


def handle_possible_url(url: str) -> str:
    parsed_url: ParseResult = urlparse(url)
    match parsed_url.scheme:
        case "http":
            return handle_web(parsed_url)
        case "https":
            return handle_web(parsed_url)
        case "file":
            return handle_file(parsed_url)
        case _:
            return url


class Hydrator:
    """
    Hydrator is in charge of receiving a tuple[str] and turning it into a dict
    suitable for a Jinja2 rendering, str being string of format of key=value, where value can be
    a literal string or URL like https:// for the web or file:// for file contents 
    """

    def __init__(self, defines: tuple[str, ...]):
        self.defines = defines

    
    def dict(self) -> dict[str,str]:
        # ("key=val=1=2",) -> { "key": "val=1=2", }
        parsed_defs: dict[str,str] = dict([d.split("=", 1) for d in self.defines])
        parsed_vals: dict[str,str] = {k : handle_possible_url(v) for k, v in parsed_defs.items()}
        return parsed_vals
    