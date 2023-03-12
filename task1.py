from deap import base, algorithms
from deap import creator
from deap import tools

import random
import matplotlib.pyplot as plt
import numpy as np

def targetFunc1(x): # функция по варианту
    return np.cos(x) / (1 + np.exp(-x))

def func_for_alg(individual): # функция по варианту, только возвращаем в виде кортежа
    return targetFunc1(individual[0]),

LOW_X, UP_X = 0.5, 10 # диапазон для поиска
ETA = 30 # используется в функциях скрещивания и мутации, определяет степень близости потомков между собой
LENGTH_CHROM = 1 # длина хромосомы, это x

# константы генетического алгоритма
POPULATION_SIZE = 30    # количество индивидуумов в популяции
P_CROSSOVER = 0.5       # вероятность скрещивания
P_MUTATION = 0.2        # вероятность мутации индивидуума
MAX_GENERATIONS = 20    # максимальное количество поколений

RANDOM_SEED = 15
random.seed(RANDOM_SEED)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def randomX(a, b): # функция для генерации случайных точек
    while True:
        randX = random.uniform(a, b)
        if(randX < 5.3 or randX > 7.5): # ограничим случайные значения, чтобы наилучшее значение не было найдено сразу
            break
    return [randX]

toolbox = base.Toolbox()

# генерируем случайные значения x
toolbox.register("randomX", randomX, LOW_X, UP_X)

# создаем функцию для создания отдельного индивидуума
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomX)

# создаем функцию для создания популяции
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

# вычисляет приспособленность каждой особи
toolbox.register("evaluate", func_for_alg)

# функция турнирного отбора
toolbox.register("select", tools.selTournament, tournsize=3)

# функция скрещивания
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=LOW_X, up=UP_X, eta=ETA)

# функция мутации
toolbox.register("mutate", tools.mutPolynomialBounded, low=LOW_X, up=UP_X, eta=ETA, indpb=1.0 / LENGTH_CHROM)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("max", np.max)
stats.register("avg", np.mean)

def extremum_individ(individuals):
    fitness_values = []
    for ind in individuals:
        fitness_values.append(ind.fitness.values[0])
    fitness_max = np.max(fitness_values)
    return [individuals[fitness_values.index(fitness_max)]]

stats_extremums = tools.Statistics(lambda ind: ind)
stats_extremums.register("extremum_individ", extremum_individ)
mstats = tools.MultiStatistics(stats=stats, extremum_individs=stats_extremums)

# создаем популяцию
population = toolbox.populationCreator(n=POPULATION_SIZE)

population, logbook = algorithms.eaSimple(population, toolbox,
                                          cxpb=P_CROSSOVER,
                                          mutpb=P_MUTATION,
                                          ngen=MAX_GENERATIONS,
                                          stats=mstats,
                                          verbose=True)

plt.figure(figsize=(10, 6)) # устанавливаем размер графика
# строим график исходной функции
plt.subplot(2, 1, 1)
x = np.arange(LOW_X, UP_X, 0.01)
plt.plot(x, targetFunc1(x))
plt.xlabel('X')
plt.ylabel('Y, значение функции')
plt.title('График функции по 11 варианту Cos(x)/ (1+exp(-x)')

extremum_individs = logbook.chapters["extremum_individs"].select("extremum_individ")
points_x = []
points_y = []
for ind in extremum_individs:
    points_x.append(ind[0][0])
    points_y.append(ind[0].fitness.values[0])

plt.scatter(points_x, points_y, marker = 'o',color = 'red', s = 40 ,label = 'Экстремумы для каждого поколения')
plt.legend(loc = 8)    # местоположение легенды
plt.grid()

# строим график работы генетического алгоритма
maxFitnessValues, meanFitnessValues = logbook.chapters["stats"].select("max", "avg")
plt.subplot(2, 1, 2)
plt.plot(maxFitnessValues, color='red',label = 'Экстремумы')
plt.plot(meanFitnessValues, color='green',label = 'Средняя приспособленность')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.legend(loc = 8)    # местоположение легенды

plt.tight_layout() # устанавливаем диапазон между графиками
plt.grid()
plt.show()
