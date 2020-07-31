from enum import Enum
from dataclasses import dataclass, field, fields, Field, MISSING, is_dataclass

import argparse


def str2bool(v):
    """
    A code snippet taken from https://stackoverflow.com/a/43357954/2726900
    """
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class CmdParsingMixin:
    """
    A mixin class that adds commandline parser manipulation methods...
    """
    @classmethod
    def create_commandline_parser(cls, description: str = None):
        """
        `MyDataClass` --> `argparse.ArgumentParser`

        This will create a commandline parser of this class's fields (or by the fields of its child class)
        """
        assert is_dataclass(cls)
        if description is None:
            description = 'Creating {} instance from commandline args...'.format(cls.__name__)
        parser = argparse.ArgumentParser(description=description)

        for fld in fields(cls):
            name_args = ["--%s" % fld.name.replace("_", "-")]
            if hasattr(fld, "short_name"):
                if fld.short_name is not None:
                    name_args.append("-%s" % fld.short_name)
            if issubclass(fld.type, Enum):
                choices = [elm.name for elm in fld.type]
            else:
                choices = None

            arg_type = fld.type
            if fld.type == bool:
                arg_type = str2bool
            elif issubclass(fld.type, Enum):
                arg_type = str

            default = fld.default
            if issubclass(fld.type, Enum):
                default = fld.default.name

            required = fld.default == MISSING

            help = None
            if hasattr(fld, "help"):
                if fld.help is not None:
                    help = fld.help

            parser.add_argument(*name_args, type=arg_type, choices=choices, help=help, default=default,
                                required=required)

        return parser

    @classmethod
    def commandline_args(cls, print_help: bool = False, description: str = None):
        """
        This will create a Namespace with commandline parser args...
        """
        parser = cls.create_commandline_parser(description)
        if print_help:
            parser.print_help()
        return parser.parse_args()

    @classmethod
    def process_commandline_args(cls, args: argparse.Namespace):
        """
        This will convert a Namespace with commandline parser args to a dataclass instance with its data...

        Args:
            args: :class:`argparse.Namespace`
        """
        assert is_dataclass(cls)

        arg_dict = vars(args)
        kwargs = {}

        for fld in fields(cls):
            argument = arg_dict[fld.name]
            if issubclass(fld.type, Enum):
                argument = fld.type[argument]
            kwargs[fld.name] = argument

        settings = cls(**kwargs)
        return settings

    @classmethod
    def build_from_commandline(cls, print_help: bool = False, description: str = None):
        """
        Args:
            print_help (bool):
            description(str):
        Returns:
            dataclass: an instnace of dataclass built by commandline_args
        """

        args = cls.commandline_args(print_help=print_help, description=description)
        settings = cls.process_commandline_args(args)

        return settings

class CmdField(Field):
    __slots__ = ('name',
                 'type',
                 'default',
                 'default_factory',
                 'repr',
                 'hash',
                 'init',
                 'compare',
                 'short_name',
                 'help',
                 'metadata',
                 '_field_type',  # Private: not to be used by user code.
                 )

    def __init__(self, default, default_factory, init, repr, hash, compare, short_name, help, metadata):
        super().__init__(default=default, default_factory=default_factory, init=init, repr=repr, hash=hash,
                         compare=compare, metadata=metadata)
        self.short_name = short_name
        self.help = help


def cmd_field(*, default=MISSING, default_factory=MISSING, init=True, repr=True,
          hash=None, compare=True, short_name=None, help=None, metadata=None):
    """
    Args:
        default: same as in conveitional :function:`field` function = )
        default_factory: same
        init: same
        repr: same
        hash: same
        compare: same
        short_name: a short name abbreviation for commandline parser ()
        help: a help message for this argument for commandline parser
        metadata: also same as in conveitional :function:`field` function = )
    Returns:
        :class:`CmdField`
    """
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    return CmdField(default, default_factory, init, repr, hash, compare, short_name=short_name, help=help,
                    metadata=metadata)
