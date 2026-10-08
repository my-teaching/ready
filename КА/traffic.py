import numpy as np
import matplotlib.pyplot as plt

ROAD_LENGTH = 100       # Длина дороги (количество клеток)
TIME_STEPS = 100        # Время симуляции (количество тактов)
V_MAX = 5               # Максимальная скорость машин (клеток за такт)
DENSITY = 0.25          # Плотность потока (доля занятых клеток от 0.0 до 1.0)
PROB_SLOWDOWN = 0.8     # Вероятность случайного торможения (человеческий фактор)


# Создаем пустую историю дороги: строки - время, столбцы - координаты.
# Значение -1 означает пустую клетку. Значения >= 0 - это скорость машины.
history = np.full((TIME_STEPS, ROAD_LENGTH), -1)

# Расставляем машины на нулевом такте времени (случайным образом)
# Начальная скорость каждой машины равна 0
num_cars = int(ROAD_LENGTH * DENSITY)
initial_positions = np.random.choice(ROAD_LENGTH, num_cars, replace=False)
history[0, initial_positions] = 0

# Цикл
for t in range(TIME_STEPS - 1):
    current_road = history[t].copy()
    next_road = np.full(ROAD_LENGTH, -1)
    
    # Находим индексы (координаты) всех машин на текущем шаге
    car_indices = np.where(current_road != -1)[0]
    
    for idx in car_indices:
        v = current_road[idx]
        
        # Вычисляем дистанцию 'd' до следующей машины с учетом закольцованности
        next_car_idx = (idx + 1) % ROAD_LENGTH
        d = 1
        while current_road[next_car_idx] == -1 and d < ROAD_LENGTH:
            d += 1
            next_car_idx = (next_car_idx + 1) % ROAD_LENGTH
            
        # ПРАВИЛО 1: Ускорение
        if v < V_MAX:
            v += 1
            
        # ПРАВИЛО 2: Торможение перед препятствием
        if v >= d:
            v = d - 1
            
        # ПРАВИЛО 3: Случайное замедление (человеческий фактор)
        if v > 0 and np.random.rand() < PROB_SLOWDOWN:
            v -= 1
            
        # ПРАВИЛО 4: Движение
        new_position = (idx + v) % ROAD_LENGTH
        next_road[new_position] = v
        
    # Записываем новое состояние дороги в матрицу истории
    history[t + 1] = next_road



plt.figure(figsize=(12, 8))

# Настраиваем цветовую палитру: 
# Белый - пустая дорога. Темные цвета - низкая скорость. Яркие - высокая.
cmap = plt.cm.viridis
cmap.set_under('white')

# Рисуем диаграмму (ось X - дорога, ось Y - время, идущее сверху вниз)
plt.imshow(history, cmap=cmap, vmin=0, vmax=V_MAX, aspect='auto', interpolation='none')
plt.colorbar(label='Скорость машины (0 - стоит, V_MAX - едет быстро)')

plt.title(f"Трафик: Плотность={DENSITY}, Вероятность торможения={PROB_SLOWDOWN}")
plt.xlabel("Координата на дороге (Пространство)")
plt.ylabel("Время (Такты)")
plt.show()