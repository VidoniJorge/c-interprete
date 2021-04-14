from typing import (
    cast,
    Dict
)

from lpp.object import (
    Builtin,
    Error,
    Integer,
    Object,
    String,
)

_UNSOPPORTED_ARGUMENT_TYPE = 'argumento para longitud sin soporte, se recibió {}'
_WROMG_NUMBER_OF_ARGS = 'número incorrecto de argumentos para longitud, se recibieron {}, se requiere {}'


def longitud(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WROMG_NUMBER_OF_ARGS.format(len(args), 1), 0)
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return Integer(len(argument.value))
    else:
        return Error(_UNSOPPORTED_ARGUMENT_TYPE.format(args[0].type().name), 0)

BUILTINS: Dict[str, Builtin] = {
    'longitud' : Builtin(fn=longitud),
}