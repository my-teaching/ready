#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <thread>
#include <chrono>

using namespace std;

const int WIDTH = 60;
const int HEIGHT = 30;
const int NUM_AGENTS = 50;
const double DT = 0.5;
const double INFECT_DIST = 2.0;

struct Agent {
    double x, y, vx, vy;
    bool infected;
};

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> pos_x(1.0, WIDTH - 2.0);
    uniform_real_distribution<> pos_y(1.0, HEIGHT - 2.0);
    uniform_real_distribution<> vel(-1.0, 1.0);

    vector<Agent> agents(NUM_AGENTS);
    for (int i = 0; i < NUM_AGENTS; ++i) {
        agents[i] = {pos_x(gen), pos_y(gen), vel(gen), vel(gen), (i == 0)};
    }

    // ANSI коды: очистка экрана и скрытие курсора
    cout << "\033[2J\033[?25l";

    while (true) {
        // Движение
        for (auto& a : agents) {
            a.x += a.vx * DT;
            a.y += a.vy * DT;
            if (a.x <= 0 || a.x >= WIDTH - 1) a.vx *= -1;
            if (a.y <= 0 || a.y >= HEIGHT - 1) a.vy *= -1;
        }

        // Заражение
        for (int i = 0; i < NUM_AGENTS; ++i) {
            for (int j = i + 1; j < NUM_AGENTS; ++j) {
                if (agents[i].infected != agents[j].infected) {
                    double dx = agents[i].x - agents[j].x;
                    double dy = agents[i].y - agents[j].y;
                    if (sqrt(dx*dx + dy*dy) < INFECT_DIST) {
                        agents[i].infected = true;
                        agents[j].infected = true;
                    }
                }
            }
        }

        // Рендер в буфер
        vector<string> screen(HEIGHT, string(WIDTH, ' '));
        vector<vector<bool>> inf_map(HEIGHT, vector<bool>(WIDTH, false));

        for (const auto& a : agents) {
            int ix = round(a.x);
            int iy = round(a.y);
            if (ix >= 0 && ix < WIDTH && iy >= 0 && iy < HEIGHT) {
                screen[iy][ix] = 'O';
                if (a.infected) inf_map[iy][ix] = true;
            }
        }

        // Перемещаем курсор в левый верхний угол (ANSI код)
        cout << "\033[H"; 
        
        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                if (screen[y][x] == 'O') {
                    // Красный (\033[31m) для больных, Синий (\033[36m) для здоровых
                    if (inf_map[y][x]) cout << "\033[31mO\033[0m";
                    else cout << "\033[36mO\033[0m";
                } else {
                    cout << ' ';
                }
            }
            cout << "\n";
        }
        cout << "Agents: " << NUM_AGENTS << " | C++ Console ABM Simulation\n";

        // Пауза 50мс
        this_thread::sleep_for(chrono::milliseconds(50));
    }
    return 0;
}