tab_len = 2

gap_symbols = "\n\r\t "
COMPLEX_TYPES = [list, dict]


class YamlParser:
    def dumps(self, obj):
        return self.__dumps(obj, 0)

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def loads(self, s):
        return self.loads_dict(s, 0, 0)[0]

    def load(self, fp):
        return self.loads(fp.read())

    def __dumps(self, obj, depth):
        response = ""
        if type(obj) is dict:
            for key, value in obj.items():
                response += " " * tab_len * depth
                response += self.obj_to_str(key) + ": "
                if type(value) in COMPLEX_TYPES:
                    response += '\n'
                response += self.__dumps(value, depth + 1)
                if type(value) not in COMPLEX_TYPES:
                    response += '\n'
        elif type(obj) is list:
            for value in obj:
                response += " " * tab_len * (depth - 1) + '-'
                if type(value) not in COMPLEX_TYPES:
                    response += ' ' + self.__dumps(value, depth)
                else:
                    response += self.__dumps(value, depth)[tab_len * (depth - 1) + 1:]
                if type(value) not in COMPLEX_TYPES:
                    response += '\n'
        else:
            return self.obj_to_str(obj)
        return response

    def loads_dict(self, s, current, depth, flag=False):
        response = {}
        while True:
            prev_current = current
            line, current = self.read_until_symbol(s, current, '\n')
            if current == len(s):
                return response, current
            if ':' not in line:
                return self.loads_list(s, prev_current, depth)
            key, value = line.split(':')
            if max(0, depth - 1) * tab_len < len(key) and key[max(0, depth - 1) * tab_len] == '-':
                if not flag:
                    return self.loads_list(s, prev_current, depth)
                else:
                    return response, prev_current

            if not self.get_spaces_count(key) == depth * tab_len:
                return response, prev_current

            key = self.str_to_obj(self.trim(key))
            value = self.trim(value)

            if len(value) > 0:
                response[key] = self.str_to_obj(value)
                current += 1
            else:
                response[key], current = self.loads_dict(s, current + 1, depth + 1)
                if flag:
                    return response, current
                continue

    def loads_list(self, s, current, depth):
        response = []
        while True:
            if current >= len(s):
                return response, current
            prev_current = current
            line, current = self.read_until_symbol(s, current, '\n')
            if '-' not in line:
                return response, prev_current
            if not line[max(0, (depth - 1)) * tab_len] == '-':
                return response, prev_current
            if ':' not in line:
                line = line[0:max(0, (depth - 1)) * tab_len] + ' ' + line[max(0, (depth - 1)) * tab_len + 1:]
                response.append(self.str_to_obj(self.trim(line)))
                current += 1
                continue

            if line[max(0, (depth - 1)) * tab_len] == '-':
                s = s[0:prev_current + max(0, (depth - 1)) * tab_len] + ' ' + s[prev_current + max(0, (
                        depth - 1)) * tab_len + 1:]
                resp, current = self.loads_dict(s, prev_current, depth, True)
                response.append(resp)
                continue

    def get_spaces_count(self, s):
        i = 0
        while i < len(s) and s[i] == ' ':
            i += 1
        return i

    def read_until_symbol(self, text, current, symbols):
        res = ""
        while len(text) > current and not text[current] in symbols:
            res += text[current]
            current += 1
        return res, current

    def trim(self, s):
        l, r = -1, 0
        for i in range(len(s)):
            if l == -1 and not s[i] in gap_symbols:
                l = i
            if not s[i] in gap_symbols:
                r = i + 1
        return s[l:r]

    def obj_to_str(self, obj):
        if type(obj).__name__ == 'str':
            return "\'" + str(obj) + "\'"
        if type(obj).__name__ == 'bool':
            return str(obj).lower()
        if obj is None:
            return "null"
        return str(obj)

    def str_to_obj(self, s):
        if s[0] == "'" and s[0] == s[-1]:
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
