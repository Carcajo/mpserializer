import toml
standard_types = ["int", "float", "bool", "str", "None"]
transfer = "\n"
gap_symbols = "\n\r\t "


class TomlParser:
    def dumps(self, obj):
        self.replace_null(obj)
        return toml.dumps(obj)
        # return self.inner_dumps(obj)

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def loads(self, s):
        res = toml.loads(s)
        self.replace_null_back(res)
        # print(res)
        return res

        # print(res)
        # return res

    def load(self, fp):
        return self.loads(fp.read())


    def replace_null(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if value is None:
                    obj[key] = "null"
                self.replace_null(value)
        if isinstance(obj, list):
            for i in range(len(obj)):
                if obj[i] is None:
                    obj[i] = "null"
                self.replace_null(obj[i])

    def replace_null_back(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if value == "null":
                    obj[key] = None
                else:
                    self.replace_null_back(value)

        if isinstance(obj, list):
            for i in range(len(obj)):
                if obj[i] == "null":
                    obj[i] = None
                else:
                    self.replace_null_back(obj[i])
    #
    # def add_double_slash(self, str):
    #     res = ""
    #     for i in range(len(str)):
    #         if str[i] == '\\':
    #             res += '\\\\'
    #         else:
    #             res += str[i]
    #     return res
    #
    # def obj_to_str(self, obj):
    #     if type(obj).__name__ == 'str':
    #         return "\"" + self.add_double_slash(str(obj)) + "\""
    #     if type(obj).__name__ == 'bool':
    #         return str(obj).lower()
    #     if obj == None:
    #         return "\"null\""
    #     if isinstance(obj, list):
    #         res = '['
    #         for i in range(len(obj)):
    #             res += self.obj_to_str(obj[i]) + ", "
    #         return res + ']'
    #     return str(obj)
    #
    # def str_to_obj(self, s):
    #     if s[0] == '[' and s[-1] == ']':
    #         res = []
    #         for item in s[1:-3].split(','):
    #             res.append(self.str_to_obj(self.trim(item)))
    #         return res
    #     # if s == '\"null\"':
    #     #     return None
    #     if s[0] == '"' and s[0] == s[-1]:
    #         return s[1:-1]
    #     if s == 'false':
    #         return False
    #     if s == 'true':
    #         return True
    #     try:
    #         return int(s)
    #     except:
    #         try:
    #             return float(s)
    #         except:
    #             return str(s)
