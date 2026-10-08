using System;
using System.Collections.Generic;
using System.Linq;

class PostMachine
{
    private HashSet<int> _tape;
    private int _head;
    private Dictionary<int, object[]> _program;
    private int _currentLine;

    public PostMachine(IEnumerable<int> tapeIndices, Dictionary<int, object[]> program, int startHead = 0)
    {
        _tape = new HashSet<int>(tapeIndices);
        _head = startHead;
        _program = program;
        _currentLine = 1;
    }

    public List<int> Run()
    {
        while (true)
        {
            if (!_program.ContainsKey(_currentLine))
            {
                Console.WriteLine("Ошибка: строка не найдена в программе.");
                break;
            }

            object[] instruction = _program[_currentLine];
            string command = (string)instruction[0];

            if (command == "!") // Стоп
            {
                Console.WriteLine("Программа завершена.");
                break;
            }
            else if (command == "->") // Вправо
            {
                _head++;
                _currentLine = (int)instruction[1];
            }
            else if (command == "<-") // Влево
            {
                _head--;
                _currentLine = (int)instruction[1];
            }
            else if (command == "V") // Поставить метку
            {
                _tape.Add(_head);
                _currentLine = (int)instruction[1];
            }
            else if (command == "x") // Стереть метку
            {
                _tape.Remove(_head);
                _currentLine = (int)instruction[1];
            }
            else if (command == "?") // Переход
            {
                if (_tape.Contains(_head))
                    _currentLine = (int)instruction[1];
                else
                    _currentLine = (int)instruction[2];
            }
        }

        var result = _tape.ToList();
        result.Sort();
        return result;
    }
}

class Program
{
    static void Main()
    {
        // Описание программы сложения
        var additionProgram = new Dictionary<int, object[]>
        {
            { 1, new object[] { "->", 2 } },
            { 2, new object[] { "?", 1, 3 } },
            { 3, new object[] { "V", 4 } },
            { 4, new object[] { "->", 5 } },
            { 5, new object[] { "?", 4, 6 } },
            { 6, new object[] { "<-", 7 } },
            { 7, new object[] { "x", 8 } },
            { 8, new object[] { "!" } }
        };

        // Начальные индексы меток
        int[] initialTape = { 0, 1, 3, 4, 5 };

        PostMachine pm = new PostMachine(initialTape, additionProgram, 0);
        List<int> result = pm.Run();

        Console.WriteLine($"Итоговые индексы меток: [{string.Join(", ", result)}]");
        Console.WriteLine($"Количество меток (результат): {result.Count}");
    }
}
