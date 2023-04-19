from types import FunctionType, CodeType
import inspect
standard_types = ["int", "float", "bool", "str", "None"]
standard_iterable_types = ["list", "tuple", "set"]
types_to_classes = {"int": int, "float": float, "bool": bool, "str": str, "None": None,
                    "list": list, "tuple": tuple, "set": set, "dict": dict}
CODE_ATTRS = (
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
)


def serialize(obj):
    response = {}
    if obj is None:
        return {"None": None}
    if type(obj) == FunctionType:
        return {"func": serialize(serialize_function(obj))}
    if type(obj).__name__ in standard_types:
        response = {type(obj).__name__: obj}
    elif type(obj).__name__ in standard_iterable_types:
        res_list = []
        for item in obj:
            res_list.append(serialize(item))
        response = {type(obj).__name__: res_list}
    elif type(obj).__name__ == 'dict':
        res_dict = {}
        i = 0
        for key, value in obj.items():
            res_dict["item" + str(i)] = {"key": serialize(key), "value": serialize(value)}
            i += 1
        response = {type(obj).__name__: res_dict}
    return response


def deserialize(obj):
    response = None
    if type(obj).__name__ == 'dict':
        if len(obj) == 1 and 'dict' in obj:
            response = {}
            for key, item in obj['dict'].items():
                 response[deserialize(item['key'])] = deserialize(item['value'])
        elif len(obj) == 1 and 'func' in obj:
            return deserialize_function(deserialize(obj["func"]))
        else:
            for key, value in obj.items():
                response = create_standard_type(key, deserialize(value))
                return response
    if type(obj).__name__ in standard_iterable_types:
        response = []
        for item in obj:
             response.append(deserialize(item))

    if response is None:
        return str(obj)
    else:
        return response


def create_standard_type(typename, value):
    if typename == "None":
        return None
    else:
        return types_to_classes[typename](value)


def serialize_function(func):
    members = dict(inspect.getmembers(func))
    code_attrs = dict(inspect.getmembers(members['__code__']))
    special = []
    for attr_name in CODE_ATTRS:
        if attr_name == 'co_lnotab' or attr_name == 'co_code':
            if len(list(code_attrs[attr_name])) == 0:
                special.append(None)
            else:
                special.append(list(code_attrs[attr_name]))
        else:
            if code_attrs[attr_name] == ():
                special.append(None)
            else:
                special.append(code_attrs[attr_name])

    name = members['__name__']
    globals_res = {"__name__": name}
    for outer_obj_name in code_attrs['co_names']:
        if outer_obj_name == name:
            globals_res[outer_obj_name] = outer_obj_name
            continue
        if outer_obj_name in __builtins__:
            continue
        globals_res[outer_obj_name] = serialize(members['__globals__'][outer_obj_name])
    # print(special)
    return {"__code__": special, "__globals__": globals_res, "__name__": name,
            "__defaults__": members['__defaults__']}


def deserialize_function(obj):
    recursive_flag = False
    globals = obj['__globals__']
    for outer_obj_name, outer_obj in globals.items():
        if outer_obj_name == obj['__name__']:
            recursive_flag = True
        globals[outer_obj_name] = deserialize(outer_obj)
    globals['__builtins__'] = __builtins__

    code = obj['__code__']
    for i in range(len(code)):
        # co_lnotab
        if i == 13 and code[i] is None:
            code[i] = b''
        if code[i] is None:
            code[i] = ()
        elif isinstance(code[i], list):
            code[i] = bytes(code[i])
    func = FunctionType(CodeType(*code), globals,
                    obj['__name__'], obj['__defaults__'], None)
    if recursive_flag:
        func.__getattribute__('__globals__')[obj['__name__']] = func
    return func
