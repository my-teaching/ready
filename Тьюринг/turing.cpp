#include <iostream>
#include <map>
#include <string>

struct Step {
    char write;
    char move;
    int next_line;
};

class TuringSimple {
    std::string tape;
    int head = 0;
    int line = 1;

public:
    TuringSimple(std::string t) : tape(t) {}

    void run(std::map<int, std::map<char, Step>> prog) {
        while (prog.count(line)) {
            char current = tape[head];
            Step s = prog[line][current];

            tape[head] = s.write;
            head += (s.move == 'R') ? 1 : -1;
            line = s.next_line;

            if (head < 0) { tape = " " + tape; head = 0; }
            if (head >= tape.size()) { tape += " "; }
        }
        std::cout << "Result: " << tape << std::endl;
    }
};

int main() {
    

    TuringSimple tm(".... ");
    tm.run(std::map<int, std::map<char, Step>>);
    return 0;
}
