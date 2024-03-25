from collections import Counter
import sys


class Arhivator:
    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def read_f(self, file):  # Функция для чтения файла
        f = open(file, 'r', encoding='utf-8')
        data = f.read()
        f.close
        return data

    def count_symbols(self):  # Подсчет количество всех символов в тексте
        data = self.read_f(self.file)
        counts = {}
        codes = {}
        for pair in Counter(data).most_common():
            counts[pair[0]] = pair[1]
            codes[pair[0]] = ''
        return counts, codes

    def make_haff_code(self, count_symbols, code_symbols):  # Получение кода каждого символа
        if len(count_symbols) == 1:
            return code_symbols
        else:
            counter = Counter(count_symbols).most_common()[:-3:-1]
            symbol1, symbol2 = counter[0][0], counter[1][0]
            for i in symbol1:
                code_symbols[i] = '0' + code_symbols[i]
            for j in symbol2:
                code_symbols[j] = '1' + code_symbols[j]
            count1, count2 = counter[0][1], counter[1][1]
            del count_symbols[symbol1]
            del count_symbols[symbol2]
            count_symbols[symbol1 + symbol2] = count1 + count2
            return self.make_haff_code(count_symbols, code_symbols)

    def create_text(self):
        if self.mode == '-e':
            text = self.read_f(self.file)
            counts, codes = self.count_symbols()
            code = self.make_haff_code(count_symbols=counts, code_symbols=codes)
            final_text, length = self.encode(text, code)
            with open(self.file.replace('txt', 'par'), 'w') as f_w:
                f_w.write(f"{length}'")
                for key, val in code.items():
                    f_w.write(str(ord(key)))
                    f_w.write('/')
                    f_w.write(val)
                    f_w.write("'")
                f_w.write('\n')

            with open(self.file.replace('txt', 'par'), 'ab') as f_wb:
                f_wb.write(final_text)
        else:
            with open(self.file, 'rb') as f_d:
                f_line = f_d.readline().decode('utf-8').strip('\n').split("'")
                encoding = f_line[1:-1]
                length = int(f_line[0])
                kod = self.dekod(encoding)
                slices = self.detext(f_d)
                text = self.decode(slices, kod, length)

            with open(self.file.replace('par', 'txt'), 'w', encoding='utf8') as f_w:
                f_w.write(text)

    def encode(self, text_in, code):  # Шифрование текста
        text_out = ''
        for let in text_in:
            text_out += code[let]
        slice = ''
        slices = []
        for i in text_out:
            if len(slice) == 8:
                slices.append(slice)
                slice = ''
            slice += i
        slices.append(slice)
        length = len(slice)
        result = bytes([int(j, 2) for j in slices])
        return result, length

    def dekod(self, encoding):  # Получение кода
        kod = {}
        for i in encoding:
            key, el = chr(int(i.split('/')[0])), i.split('/')[1]
            kod[el] = key
        return kod

    def detext(self, f):  # Получение текста
        text = []
        for line in f:
            text += [ord(i) for i in line.decode('latin-1')]
        return text

    def decode(self, slices, kod, length):  # Дешифрование текста
        text = []
        for i, val in enumerate(slices, start=1):
            slice = bin(val)[2:]
            if len(slice) < 8 and i != len(slices):
                while len(slice) < 8:
                    slice = '0' + slice
            elif i == len(slices) and len(slice) < length:
                while len(slice) < length:
                    slice = '0' + slice
            text.append(slice)
        text = ''.join(text)
        let = ''
        text_out = ''
        for j in text:
            let += j
            if let in kod:
                text_out += kod[let]
                let = ''
        return text_out


parametrs = []
for parametr in sys.argv:
    if parametr != 'main.py':
        parametrs.append(parametr)
mode = parametrs[0]
file = parametrs[1]
arhivator = Arhivator(file, mode)
arhivator.create_text()
