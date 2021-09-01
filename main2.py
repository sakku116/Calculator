from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
import math

# set window size
Window.size = (270, 540)

# load kv lang file
Builder.load_file('calc_design.kv')

class CalcLayout(Widget):
    error_text = 'ERROR'

    def clear(self):
        self.ids.output_label.text = ''
        self.ids.output_history.text = ''
        self.ids.output_label.font_size = 30

    def delete(self):
        output = self.ids.output_label.text
        if CalcLayout.error_text in output:
            self.ids.output_label.text = ''

        else:
            # menghapus karakter terakhir
            output = output[:-1]

            self.ids.output_label.text = output

    def button_press(self, char):
        count = 0
        # Menagkap teks dari outputlabel
        output = self.ids.output_label.text

        # MENGHITUNG JUMLAH OPEN BRACKET DAN CLOSE BRACKET
        ###################################
        def brackets_len(char):
            closed_bracket = []
            for i in list(output):
                if i == char:
                    closed_bracket.append(i)
            result = len(closed_bracket)
            return result

        openBracket_total = brackets_len('(')
        closeBracket_total = brackets_len(')')
        ####################################

        #log
        print(f'openBracket_total = {openBracket_total}', f'closeBracket_total = {closeBracket_total}')

        if CalcLayout.error_text in output:
            self.ids.output_label.text = ''
            self.ids.output_label.text += f'{char}'
        else:
            str_list = list(output)
            if output.find(')') != 0:
                if char == '√':
                    char = '√()'
                self.ids.output_label.text += f'{char}'
            count -= closeBracket_total
            if output.find(')') != -1:
                #log
                print(f'insert char index if close bracket in output = {count}')

                str_list.insert(count, char)
                # replace semua karaker di dalam dictionary
                replace_chars = {
                    "[": "",
                    "]":"",
                    "'":"",
                    ",":"",
                    " ":""}
                for i, j in replace_chars.items():
                    str_list = str(str_list).replace(i, j)

                self.ids.output_label.text = str_list

    def equals_button(self):
        # menaruh input text ke dalam history label
        pre_output = self.ids.output_label.text
        if pre_output == CalcLayout.error_text:
            pass
        else:
            self.ids.output_history.text = pre_output

        output = pre_output.replace(',','')

        # MENCARI INDEX DARI OPEN BRACKET DAN CLOSE BRACKET
        ####################################
        def find_brackets_index(char):
            index = 0
            openBracket_index = []
            while index < len(pre_output):
                index = pre_output.find(char, index)
                if index == -1:
                    break
                else:
                    openBracket_index.append(index)
                    index += 1
            return openBracket_index

        openBracket_index = find_brackets_index('(')
        closeBracket_index = find_brackets_index(')')
        ####################################

        #log
        print(f'openBracket_index = {openBracket_index}', f'closeBracket_index = {closeBracket_index}')

        # replace semua karaker di dalam dictionary
        replace_chars = {
            "×": "*",
            "÷":"/",
            "^":"**"}
        for i, j in replace_chars.items():
            output = output.replace(i, j)

        if '√' in output:
            print(output.split('√'))
            def sqrtmath_solver(get):
                output = get
                # mencari index √ dari output
                find_sqrt = output.find('√')
                # mendapatkan string setelah tanda sqrt dari output
                str_aft_sqrt = output[find_sqrt+1:]
                # menyelesaikan masalah sqrt di str_aft_sqrt
                sqrt_solver = math.sqrt(int(str_aft_sqrt))
                # mereplace str_aft_sqrt dengan sqrt_solver
                output = output.replace(str_aft_sqrt, str(sqrt_solver))
                if '+' in output[find_sqrt-2:find_sqrt]:
                    output = output.replace('√','')
                    return output
                else:
                    output = output.replace('√','*')
                    return output
            sqrt_output = sqrtmath_solver(output)
            result = str(eval(sqrt_output)).replace('.0','')

            print(f'{output} = {result}')

class MyCalculatorApp(App):
    def build(self):
        return CalcLayout()
if __name__ == '__main__':
    MyCalculatorApp().run()
