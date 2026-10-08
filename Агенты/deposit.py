import matplotlib.pyplot as plt

# dS / dt = v

# 1. Параметры
S = 0          # Сумма в копилке (начальная)
v = 150        # Скорость пополнения (руб/день)
dt = 0.001         # Шаг времени (1 день)
days = 30      # Общий срок

# Списки для графика
history_S = [S]
history_t = [0]

# 2. Цикл накопления (Метод Эйлера)
t = 0
while t < days:
    # Сумма = Старая сумма + (Скорость * Шаг времени)
    S = S + v * dt
    t = t + dt
    
    history_S.append(S)
    history_t.append(t)

# 3. Вывод результата
print(f"Итого в копилке через {days} дней: {S} руб.")

# 4. График
plt.plot(history_t, history_S, marker='o', color='gold')
plt.title("Накопление денег в копилке")
plt.xlabel("Дни")
plt.ylabel("Рубли")
plt.grid(True)
plt.show()