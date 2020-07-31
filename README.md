argparse_dataclasses
=====================

In this package we'll place some boilerplate code that helps:
 
 - to convert `dataclasses` to `argparse` commandline argument parsers;
 - to convert `argparse` commandline arguments to `dataclasses`.

Why so?
Dozens of times I had to create settings classes for my Python console scripts. Here's some utility boilerplate code that helps to create commandline parsers for dataclasses in a couple of lines = )


How to install
---------------

    python3 -m pip install argparse-dataclasses

How to use
--------------

At first, let's create a simple script `simple_example.py`, in which we:
- import some stuff from our module,
- declare a simple `dataclass`
- and inherit it from our `CmdParsingMixin` (this adds support for automatic `argparse.ArgumentParser` creation.

`simple_example.py`
```

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

 ```

And let's run this script from commandline:

`> python3 simple_example.py`

It will give us the error message.

<span style="color:red">

```
usage: simple_example.py [-h] --name NAME [--num-experiments NUM_EXPERIMENTS]
simple_example.py: error: the following arguments are required: --name
```
</span>

Okay, just as planned. As we can see, we've forgot a required commandline argument. Let's try again

    > python3 simple_example.py --name=DJ_BLYATMAN --num-experiments=33

This will print us the settings instance:
    
    SimpleSettings(name='DJ_BLYATMAN', num_experiments=33)
    
Be careful: use `-` in commandline argument names and `_` in Python dataclass field names. It does make sense!

Our code works with `argparse.ArgumentParser` under the hood, so it also supports `--help` commandline argument to explicitly order help message:

    > python3 simple_example.py --help
will output the following:

```
usage: simple_example.py [-h] --name NAME [--num-experiments NUM_EXPERIMENTS]

Creating SimpleSettings instance from commandline args...

optional arguments:
  -h, --help            show this help message and exit
  --name NAME
  --num-experiments NUM_EXPERIMENTS``
```
 
