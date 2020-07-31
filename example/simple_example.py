
from dataclasses import dataclass, field
from argparse_dataclasses import CmdParsingMixin


@dataclass
class SimpleSettings(CmdParsingMixin): #
    # A simple field (will be converted to required commandline argument, 'cause it has no default value...)
    name: str

    # And a true dataclass field (it has a default value and will be converted to non-required argument)
    num_experiments: int = field(default=1)

# Here we create a cute commandline arg parser with args same as our dataclass fields
# We parse the commandline arguments (if incorrect arguments were input to console, it gives a good error message)
# And we create an instance of our SimpleSettings class by our arguments

# And here we create a `SimpleSettings` instance from commNamespace of commandline args:
settings = SimpleSettings.build_from_commandline()

print(settings)
