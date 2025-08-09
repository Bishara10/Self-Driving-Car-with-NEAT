import os

import neat
import visualize
from game import Game
from numpy import argmax

generation = 1

def train(genomes, config):
    global generation
    nets = [] # keep track of neural networks
    ge = [] # keep track of genomes
    population_size = len(genomes)

    for genome_id, genome in genomes:
        genome.fitness = 0
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)


    game = Game(population_size)

    actions = [0] * population_size # initialize actions to no action for each car
    while True:
        nearest_collision_points_distances, destroyed_cars_indices = game.step(actions, generation)
        i = 0
        for index in destroyed_cars_indices:
            ge.pop(index-i)
            nets.pop(index-i)
            actions.pop(index-i)
            i += 1

        if len(ge) == 0:
            break

        for i, g in enumerate(ge):
            actions[i] = argmax(nets[i].activate(nearest_collision_points_distances[i]))
            g.fitness += 0.1

    # node_names = {-1: 'Sensor1', -2: 'Sensor2', -3: 'Sensor3', -4: 'Sensor4', 0: 'Forward', 1: 'Left', 2: 'Right'}
    best_genome_this_gen = max(genomes, key=lambda x: x[1].fitness)[1]
    visualize.draw_net(config, best_genome_this_gen, view=True, prune_unused=True)
    # visualize.plot_species(stats, view=False)

    generation += 1

def main(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(train, 50)

    # node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    visualize.draw_net(config, winner, True)
    visualize.draw_net(config, winner, True, prune_unused=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.ini')
    main(config_path)