import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

GRID_SIZE = 50      # Размер поля (50x50 клеток)
UPDATE_INTERVAL = 100 # Скорость обновления в миллисекундах

# Создаем поле со случайными значениями: 0 (мертва) или 1 (жива)
# Вероятность: 80% мертвых, 20% живых клеток в начале
grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.8, 0.2])

def update(frameNum, img, grid, N):
    """
    Функция, которая вызывается на каждом кадре анимации.
    Здесь происходит математическое моделирование Игры "Жизнь".
    """
    # Создаем КОПИЮ поля, куда будем записывать новые состояния
    new_grid = grid.copy()
    
    # Проходим по всем клеткам (кроме самых крайних, для простоты)
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            
            # Считаем сумму 8 соседей вокруг клетки (i, j)
            # Поскольку живая клетка это 1, а мертвая 0, сумма = количество живых соседей
            total = (grid[i-1][j-1] + grid[i-1][j] + grid[i-1][j+1] +
                     grid[i][j-1]                + grid[i][j+1] +
                     grid[i+1][j-1] + grid[i+1][j] + grid[i+1][j+1])
            
            # Правило 1 и 2: Одиночество или Перенаселение
            if grid[i][j] == 1:
                if (total < 2) or (total > 3):
                    new_grid[i][j] = 0 # Клетка умирает
            # Правило 3: Зарождение жизни
            else:
                if total == 3:
                    new_grid[i][j] = 1 # Клетка оживает
                    
    # Обновляем картинку на экране
    img.set_data(new_grid)
    # Заменяем старую матрицу на новую для следующего шага
    grid[:] = new_grid[:]
    return img,


fig, ax = plt.subplots()
plt.title("Математическая модель: Игра 'Жизнь' (Клеточный автомат)")
# Отрисовываем матрицу
img = ax.imshow(grid, interpolation='nearest', cmap='binary')

# Запускаем анимацию
ani = animation.FuncAnimation(
    fig, 
    update, 
    fargs=(img, grid, GRID_SIZE), 
    frames=10, 
    interval=UPDATE_INTERVAL, 
    save_count=50
)

plt.show()