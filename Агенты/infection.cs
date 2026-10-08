using System;
using System.Collections.Generic;
using System.Threading;

namespace AgentSim
{
    class Program
    {
        const int WIDTH = 60;
        const int HEIGHT = 30;
        const int NUM_AGENTS = 50;
        const double DT = 0.5;
        const double INFECT_DIST = 2.0;

        class Agent
        {
            public double x, y, vx, vy;
            public bool infected;
        }

        static void Main()
        {
            Random rnd = new Random();
            List<Agent> agents = new List<Agent>();

            for (int i = 0; i < NUM_AGENTS; i++)
            {
                agents.Add(new Agent
                {
                    x = rnd.NextDouble() * (WIDTH - 1),
                    y = rnd.NextDouble() * (HEIGHT - 1),
                    vx = rnd.NextDouble() * 2 - 1,
                    vy = rnd.NextDouble() * 2 - 1,
                    infected = (i == 0) // Первый будет больным
                });
            }

            Console.CursorVisible = false;

            while (true)
            {
                // Логика
                foreach (var a in agents)
                {
                    a.x += a.vx * DT;
                    a.y += a.vy * DT;
                    if (a.x <= 0 || a.x >= WIDTH - 1) a.vx *= -1;
                    if (a.y <= 0 || a.y >= HEIGHT - 1) a.vy *= -1;
                }

                // Инфекция
                for (int i = 0; i < agents.Count; i++)
                {
                    for (int j = i + 1; j < agents.Count; j++)
                    {
                        if (agents[i].infected != agents[j].infected)
                        {
                            double dx = agents[i].x - agents[j].x;
                            double dy = agents[i].y - agents[j].y;
                            if (Math.Sqrt(dx * dx + dy * dy) < INFECT_DIST)
                            {
                                agents[i].infected = true;
                                agents[j].infected = true;
                            }
                        }
                    }
                }

                // Отрисовка
                Console.SetCursorPosition(0, 0); // Не Clear(), чтобы не мерцало
                char[,] buffer = new char[HEIGHT, WIDTH];
                bool[,] infectedBuffer = new bool[HEIGHT, WIDTH];

                // Очистка буфера пробелами
                for (int y = 0; y < HEIGHT; y++)
                    for (int x = 0; x < WIDTH; x++)
                        buffer[y, x] = ' ';

                // Заполнение буфера агентами
                foreach (var a in agents)
                {
                    int ix = (int)a.x;
                    int iy = (int)a.y;
                    if (ix >= 0 && ix < WIDTH && iy >= 0 && iy < HEIGHT)
                    {
                        buffer[iy, ix] = 'O'; // Символ агента
                        if (a.infected) infectedBuffer[iy, ix] = true;
                    }
                }

                // Вывод на экран с цветами
                for (int y = 0; y < HEIGHT; y++)
                {
                    for (int x = 0; x < WIDTH; x++)
                    {
                        if (buffer[y, x] == 'O')
                        {
                            Console.ForegroundColor = infectedBuffer[y, x] ? ConsoleColor.Red : ConsoleColor.Cyan;
                            Console.Write('O');
                        }
                        else
                        {
                            Console.Write(' ');
                        }
                    }
                    Console.WriteLine();
                }
                
                Console.ResetColor();
                Console.WriteLine("Нажми Ctrl+C для выхода");
                Thread.Sleep(50); // Пауза 50мс (20 FPS)
            }
        }
    }
}