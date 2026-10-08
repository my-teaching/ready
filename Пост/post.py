class PostMachine:
    def __init__(self, tape_indices, program, start_head=0):
        self.tape = set(tape_indices)
        self.head = start_head
        self.program = program
        self.current_line = 1

    def run(self):
        while True:
            if self.current_line not in self.program:
                print("Ошибка: строка не найдена в программе.")
                break
            
            instruction = self.program[self.current_line]
            command = instruction[0]

            if command == '!': # Стоп
                print("Программа завершена.")
                break

            elif command == '->': # Вправо
                self.head += 1
                self.current_line = instruction[1]

            elif command == '<-': # Влево
                self.head -= 1
                self.current_line = instruction[1]

            elif command == 'V': # Поставить метку
                self.tape.add(self.head)
                self.current_line = instruction[1]

            elif command == 'x': # Стереть метку
                if self.head in self.tape:
                    self.tape.remove(self.head)
                self.current_line = instruction[1]

            elif command == '?': # Переход (если метка - 1-й переход, если пусто - 2-й)
                if self.head in self.tape:
                    self.current_line = instruction[1]
                else:
                    self.current_line = instruction[2]
        
        return sorted(list(self.tape))


pm = PostMachine([], {}, start_head=0)
result = pm.run()

