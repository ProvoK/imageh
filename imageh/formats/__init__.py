import attr


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
class Descriptor(object):
    width = attr.ib(init=False)
    height = attr.ib(init=False)
    bytes_read = attr.ib(init=False)
    format = attr.ib(init=False)
    filename = attr.ib(init=False)