from enum import IntEnum, auto
import argparse
from dataclasses import dataclass, field

from cmd_args.cmd_fields import cmd_field, CmdParsingMixin


class ExplosiveType(IntEnum):
    PENT = auto()
    TNT = auto()
    RDX = auto()
    PLASTIC = auto()
    UNKNOWN= auto()


@dataclass
class ExampleSettings(CmdParsingMixin):
    # A couple of simple fields:
    name: str  # will be converted to required commandline argument, 'cause it has no default value...
    cached_data_path: str = None  # This field will be converted to non-required argument...

    # some true dataclass fields:
    num_experiments: int = field(default=1)  # Will be also converted to non-required argument

    # and some `cmd_field`s with extra arguments (`short_name` and `help`)
    out_path: str = cmd_field(default="out_dumps", short_name="o", help="Output dumps path")

    # and yes, we support enums too (commandline args choices will be generated)
    explosive_type: ExplosiveType = cmd_field(
        default=ExplosiveType.TNT, short_name="ex",
        help="Select correct explosive or the detonation speed will be calculated incorrectly")

#
settings = ExampleSettings(name="Setting DIMEX X-RAY detector")


if __name__ == "__main__":

    args = ExampleSettings.commandline_args(print_usage=True)
    settings = ExampleSettings.process_commandline_args(args)

    print()
    print("Args parsed:")
    print(args)

    print()
    print("Settings created:")
    print(settings)
    print("^__^")
