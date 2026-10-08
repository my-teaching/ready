using System;
using System.Linq;

class TrafficSimulation
{
    static void Main()
    {
        // Константы
        const int ROAD_LENGTH = 100;
        const int TIME_STEPS = 50; // Уменьшил для наглядности в консоли
        const int V_MAX = 5;
        const double DENSITY = 0.25;
        const double PROB_SLOWDOWN = 0.3;

        int[,] history = new int[TIME_STEPS, ROAD_LENGTH];
        Random rand = new Random();

        // Инициализация (заполняем -1)
        for (int t = 0; t < TIME_STEPS; t++)
            for (int x = 0; x < ROAD_LENGTH; x++)
                history[t, x] = -1;

        // Расставляем машины
        int numCars = (int)(ROAD_LENGTH * DENSITY);
        int placed = 0;
        while (placed < numCars)
        {
            int pos = rand.Next(ROAD_LENGTH);
            if (history[0, pos] == -1)
            {
                history[0, pos] = 0;
                placed++;
            }
        }

        // Основной цикл симуляции
        for (int t = 0; t < TIME_STEPS - 1; t++)
        {
            for (int x = 0; x < ROAD_LENGTH; x++)
            {
                int v = history[t, x];
                if (v == -1) continue; // Пусто

                // 1. Ускорение
                if (v < V_MAX) v++;

                // 2. Дистанция до следующей машины (закольцованность)
                int d = 1;
                while (history[t, (x + d) % ROAD_LENGTH] == -1 && d < ROAD_LENGTH)
                {
                    d++;
                }

                // Торможение
                if (v >= d) v = d - 1;

                // 3. Вероятностное замедление
                if (v > 0 && rand.NextDouble() < PROB_SLOWDOWN)
                {
                    v--;
                }

                // 4. Движение
                int newPos = (x + v) % ROAD_LENGTH;
                history[t + 1, newPos] = v;
            }
        }

        // Вывод в консоль (упрощенная визуализация)
        for (int t = 0; t < TIME_STEPS; t++)
        {
            for (int x = 0; x < ROAD_LENGTH; x++)
            {
                int val = history[t, x];
                Console.Write(val == -1 ? "." : val.ToString());
            }
            Console.WriteLine();
        }
    }
}
