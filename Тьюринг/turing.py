class TuringMachineSimple:
    def __init__(self, tape_str):
        self.tape = list(tape_str)
        self.head = 0
        self.line = 1

    def run(self, program):
        while self.line in program:
            char = self.tape[self.head]
            # Инструкция: {текущий_символ: (новый_символ, движение, след_строка)}
            new_char, move, next_line = program[self.line][char]
            
            self.tape[self.head] = new_char
            self.head += 1 if move == 'R' else -1
            self.line = next_line
            
            # Авто-расширение ленты
            if self.head < 0: 
                self.tape.insert(0, ' ')
                self.head = 0
            if self.head >= len(self.tape): 
                self.tape.append(' ')
        return "".join(self.tape).strip()


tm = TuringMachineSimple("....")
print(tm.run({}}))
