import importlib
from pkgutil import walk_packages

import attr


def _load_parsers_modules(root_import_path, is_valid=lambda entity: True):

    modules = []

    for _, name, is_pkg in walk_packages(root_import_path):
        if is_pkg or name.startswith('_'):
            continue

        mod = importlib.import_module('.{}'.format(name), 'imageh.formats')
        if is_valid(mod):
            modules.append(mod)

    return modules


def load():
    """
    Search for available parser in `formats` folder.
    
    :return: list of BaseParser subclasses.
    """
    has_parser_cls = lambda entity: getattr(entity, 'Parser', False)
    is_baseparser_subcls = lambda entity: issubclass(getattr(entity, 'Parser'), BaseParser)

    modules = _load_parsers_modules(
        root_import_path=__path__,
        is_valid=lambda e: has_parser_cls(e) and is_baseparser_subcls(e)
    )
    return [getattr(m, 'Parser') for m in modules]


class BaseParser(object):
    """
    TODO DOC
    """
    bytes_to_read = 0

    def __init__(self, fd, chunk):
        # type: (BinaryIO, List) -> None
        self.chunk = chunk + fd.read(self.bytes_to_read)

    @staticmethod
    def check_format(head):
        # type: (List[ByteString]) -> bool
        raise NotImplemented

    def parse(self):
        # type: () -> ImageDescriptor
        raise NotImplemented


@attr.s
class BaseDescriptor(object):
    width = attr.ib(init=False)
    height = attr.ib(init=False)
    bytes_read = attr.ib(init=False)
    format = attr.ib(init=False)
    filename = attr.ib(init=False)