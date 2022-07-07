import sys
import numpy as np
import pygad

import tools.write2tree as w
from tools.getdata import get_position, get_residuals
from tools.fitness import xyz_fit,residuals_fit


def fitness_func(solution, solution_idx):

    global ga_instance

    # print(solution_idx,solution)
    generation = ga_instance.generations_completed
    # path='/home/src2/Maria/optimizer/data'
    path='/home/WVU-AD/jgross2/optimizer/data'

    #write parameters to tree and check rtgx ran succesfully
    flag = w.write2tree(solution, solution_idx, generation, path)

    if flag != True:
        sys.exit() #if rtgx fails stop this program

    #Extract data
    x,y,z,Time = get_position(solution_idx=solution_idx, generation=generation, path=path)
    phase, TimeP, range, TimeR = get_residuals(solution_idx, generation, path)

    #Get fitness from this data
    xyzfitness=xyz_fit(x,y,z,Time)
    residualfitness=residuals_fit(phase, TimeP, range, TimeR )

    fitness=xyzfitness+residualfitness


    return fitness

fitness_function=fitness_func
last_fitness = 0
def on_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

def on_start(ga_instance):
    print("on_start()")

def on_fitness(ga_instance, population_fitness):
    print("on_fitness()")

def on_parents(ga_instance, selected_parents):
    print("on_parents()")

def on_crossover(ga_instance, offspring_crossover):
    print("on_crossover()")

def on_mutation(ga_instance, offspring_mutation):
    print("on_mutation()")



def on_stop(ga_instance, last_population_fitness):
    print("on_stop()")

ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=5,
                       fitness_func=fitness_function,
                       sol_per_pop=15,
                       num_genes=7,
                       parent_selection_type='tournament', #or 'rank'
                       K_tournament=4,
                    #    keep_parents=-1,
                       # gene_type=[[float,2],[float,2],[float,2],[float,3],int,int,[float,2],[float,2]],
                       gene_space = [[*np.arange(1.5,3,0.1)],
                       [*np.round(np.arange(0.1,0.2,0.005),3)],    #[0.195,2.3,0.5,0.005,1000,10,0.01,1]
                       [*np.round(np.arange(0.1,1,0.1),2)],
                       [*np.round(np.arange(0.01,0.2,0.01),3)],
                       range(5,2000,5),
                       range(1,600,2),
                       [*np.round(np.arange(0.01,0.4,0.01),2)]],
                       # [*np.arange(0.01,1.01,0.01)]],
                    #    save_best_solutions=True,
                       on_start=on_start,
                       on_fitness=on_fitness,
                       on_parents=on_parents,
                       on_crossover=on_crossover,
                       on_mutation=on_mutation,
                       on_generation=on_generation,
                       on_stop=on_stop,
                       mutation_probability=0.3,
                       crossover_type="single_point",
                       crossover_probability=0.7)

                    #    save_solutions=True)

print("Initial Population")
print(ga_instance.initial_population)

ga_instance.run()


# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

print("Final Population")
print(ga_instance.population)

ga_instance.plot_fitness()
# Saving the GA instance.
filename = 'tournament_crossp'
ga_instance.save(filename=filename)
