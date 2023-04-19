tab_len = 2
gap_symbols = "\n\r\t "


class JsonParser:

    def dumps(self, obj):
        return self.inner_dumps(obj)

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def loads(self, s):
        return self.inner_loads(s)[0]

    def load(self, fp):
        return self.loads(fp.read())

    def inner_dumps(self, obj, depth=1):
        if type(obj) is dict:
            res = "{\n"
            for key, value in obj.items():
                res = res + " " * tab_len * depth
                res = res + "\"" + str(key) + "\"" + ": " + self.inner_dumps(value, depth + 1) + ',\n'
            res = res[0:-2] + "\n"
            res += " " * tab_len * (depth - 1) + "}"
            return res
        elif type(obj) == list:
            res = "[\n"
            for item in obj:
                res = res + " " * tab_len * depth
                res = res + self.inner_dumps(item, depth + 1) + ',\n'
            res = res[0:-2] + "\n"
            res += " " * tab_len * (depth - 1) + "]"
            return res
        else:
            return self.obj_to_str(obj)

    def inner_loads(self, text, current=0):
        if text[current] == '{':
            return self.load_object(text, current + 1)
        else:
            return self.load_list(text, current + 1)

    def load_object(self, text, current):
        res = {}
        while True:
            key, current = self.get_key(text, current)
            value, current = self.get_value(text, current + 2)
            res[key] = value
            if text[current] == ']':
                current += 1
            current = self.read_gap_symbols(text, current + 1)
            if text[current] == '}':
                return res, current

    def load_list(self, text, current):
        res = []
        while True:
            value, current = self.get_value(text, current)
            res.append(value)
            if text[current] == '}':
                current += 1
            current = self.read_gap_symbols(text, current + 1)
            if text[current] == ']':
                return res, current

    def get_key(self, text, current):
        _, current = self.read_until_symbol(text, current, '"')
        key, current = self.read_until_symbol(text, current + 1, '"')
        return key, current

    def get_value(self, text, current):
        current = self.read_gap_symbols(text, current)
        if text[current] == '{' or text[current] == '[':
            return self.inner_loads(text, current)

        if text[current] == '"':
            value, current = self.read_until_symbol(text, current + 1, '"')
            current += 1
        else:
            value, current = self.read_until_symbol(text, current, ' ,}]\n')
        return self.str_to_obj(value), current

    def read_until_symbol(self, text, current, symbols):
        res = ""
        while not text[current] in symbols:
            res += text[current]
            current += 1
        return res, current

    def read_gap_symbols(self, text, current):
        while text[current] in gap_symbols:
            current += 1
        return current

    def obj_to_str(self, obj):
        if type(obj).__name__ == 'str':
            return "\"" + str(obj) + "\""
        if type(obj).__name__ == 'bool':
            return str(obj).lower()
        if obj == None:
            return "null"
        return str(obj)

    def str_to_obj(self, s):
        if s[0] == '"' and s[0] == s[-1]:
            return s[1:-1]
        if s == 'false':
            return False
        if s == 'true':
            return True
        if s == 'null':
            return None
        try:
            return int(s)
        except:
            try:
                return float(s)
            except:
                return str(s)
