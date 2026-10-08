import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

"""
МАТЕМАТИЧЕСКАЯ МОДЕЛЬ: ЛЕСНОЙ ПОЖАР (Клеточный автомат)
"""

GRID_SIZE = 100         # Размер леса 100x100
P_GROWTH = 0.0005         # Вероятность роста нового дерева на пустом месте (5%)
P_LIGHTNING = 0.00005    # Вероятность удара молнии в дерево (0.05%)

# Состояния нашего конечного автомата (клетки)
EMPTY = 0   # Пустая земля (Черный цвет)
TREE = 1    # Дерево (Зеленый цвет)
FIRE = 2    # Огонь (Красный цвет)


# Создаем пустую матрицу леса
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Цветовая схема для визуализации: 0-Черный, 1-Зеленый, 2-Красный
cmap = ListedColormap(['black', 'green', 'red'])

def update(frameNum, img, grid, N):
    new_grid = grid.copy()
    
    # Проходим по всем клеткам (игнорируем края для простоты)
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            
            
            # ПРАВИЛО 1: Огонь сгорает и оставляет пустошь
            if grid[i][j] == FIRE:
                new_grid[i][j] = EMPTY
                
            # ПРАВИЛО 2: Если пустая земля -> может вырасти дерево
            elif grid[i][j] == EMPTY:
                if np.random.random() < P_GROWTH:
                    new_grid[i][j] = TREE
                    
            # ПРАВИЛО 3: Дерево может загореться от соседей или от молнии
            elif grid[i][j] == TREE:
                # Проверяем 8 соседей вокруг
                neighbors =[
                    grid[i-1][j-1], grid[i-1][j], grid[i-1][j+1],
                    grid[i][j-1],                 grid[i][j+1],
                    grid[i+1][j-1], grid[i+1][j], grid[i+1][j+1]
                ]
                
                # Если хоть один сосед горит -> дерево загорается от него
                if FIRE in neighbors:
                    new_grid[i][j] = FIRE
                # Иначе, проверяем шанс удара случайной молнии
                elif np.random.random() < P_LIGHTNING:
                    new_grid[i][j] = FIRE

    # Обновляем картинку
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

fig, ax = plt.subplots(figsize=(8, 8))
plt.title("Динамическая модель Лесного Пожара (Клеточный автомат)")

img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)
ax.axis('off')

ani = animation.FuncAnimation(
    fig, 
    update, 
    fargs=(img, grid, GRID_SIZE), 
    frames=200, 
    interval=500, # Скорость смены кадров
    save_count=50
)

plt.show()

