#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <string>

struct Instruction {
    std::string cmd;
    int n1 = 0; // Первый переход
    int n2 = 0; // Второй переход (только для '?')
};

class PostMachine {
    std::set<int> tape;
    int head;
    std::map<int, Instruction> program;
    int current_line = 1;

public:
    PostMachine(std::vector<int> initial_tape, std::map<int, Instruction> prog, int start_head = 0) 
        : head(start_head), program(prog) {
        for (int x : initial_tape) tape.insert(x);
    }

    void run() {
        while (true) {
            // Проверка на наличие строки (как KeyError в Python)
            if (program.find(current_line) == program.end()) {
                std::cout << "Ошибка: строка " << current_line << " не найдена." << std::endl;
                break;
            }

            Instruction &inst = program[current_line];

            if (inst.cmd == "!") {
                std::cout << "Программа завершена." << std::endl;
                break;
            }
            else if (inst.cmd == "->") {
                head++;
                current_line = inst.n1;
            }
            else if (inst.cmd == "<-") {
                head--;
                current_line = inst.n1;
            }
            else if (inst.cmd == "V") {
                tape.insert(head);
                current_line = inst.n1;
            }
            else if (inst.cmd == "x") {
                tape.erase(head);
                current_line = inst.n1;
            }
            else if (inst.cmd == "?") {
                // Если метка есть (count > 0) -> n1, иначе -> n2
                current_line = tape.count(head) ? inst.n1 : inst.n2;
            }
        }

        // Вывод результата
        std::cout << "Итоговые метки: ";
        for (int x : tape) std::cout << x << " ";
        std::cout << std::endl;
    }
};

int main() {
    

    PostMachine pm({}, std::map<int, Instruction>);
    pm.run();

    return 0;
}
