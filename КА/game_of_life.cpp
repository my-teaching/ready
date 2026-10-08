#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

using namespace std;

const int GRID_SIZE = 40; // Чуть меньше для консоли
const int UPDATE_INTERVAL = 100;

// Отрисовка поля в консоли
void draw(const vector<vector<int>>& grid) {
    string output = "";
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            output += (grid[i][j] == 1 ? "█" : " "); // Живая - символ, мертвая - пусто
        }
        output += "\n";
    }
    // Используем ANSI-код для возврата курсора в начало (быстрее, чем system("cls"))
    cout << "\033[H" << output << flush;
}

int main() {
    // Инициализация поля
    vector<vector<int>> grid(GRID_SIZE, vector<int>(GRID_SIZE));
    srand(time(0));

    for (int i = 0; i < GRID_SIZE; ++i)
        for (int j = 0; j < GRID_SIZE; ++j)
            grid[i][j] = (rand() % 100 < 20) ? 1 : 0; // 20% живых

    while (true) {
        draw(grid);
        vector<vector<int>> next_grid = grid;

        for (int i = 1; i < GRID_SIZE - 1; ++i) {
            for (int j = 1; j < GRID_SIZE - 1; ++j) {
                // Считаем соседей
                int neighbors = 0;
                for (int x = -1; x <= 1; ++x)
                    for (int y = -1; y <= 1; ++y)
                        neighbors += grid[i + x][j + y];
                
                neighbors -= grid[i][j]; // Вычитаем саму клетку

                // Правила игры
                if (grid[i][j] == 1 && (neighbors < 2 || neighbors > 3))
                    next_grid[i][j] = 0;
                else if (grid[i][j] == 0 && neighbors == 3)
                    next_grid[i][j] = 1;
            }
        }

        grid = next_grid;
        this_thread::sleep_for(chrono::milliseconds(UPDATE_INTERVAL));
    }

    return 0;
}
