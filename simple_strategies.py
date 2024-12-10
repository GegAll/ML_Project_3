from experiment import concert_prob_per_day
from infrastucture.network import fill_network, Network
from simulation import simulate_epidemic
from vaccination import add_preferences_to_graph, attendence_prob, build_social_graph, load_friendships, \
    load_preferences, plot_epidemic_curves, print_daily_results

import numpy as np
import matplotlib.pyplot as plt
import random

def strategy_no_vaccination():
    return []


def strategy_random_vaccination():
    network = fill_network()

    all_users = list(network.users)
    sample_size = max(1, len(all_users) * 12 // 100)
    random_users = random.sample(all_users, sample_size)

    return random_users

def strategy_most_friends():
    network = fill_network()

    user_friends_count = {user: len(network.get_friends_of(user.id)) for user in network.users}
    sorted_users_by_friends = sorted(user_friends_count, key=user_friends_count.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_friends) * 12 // 100)
    top_12_percent_users = sorted_users_by_friends[:top_12_percent_count]

    return top_12_percent_users


def strategy_most_genres_interested():
    network = fill_network()

    user_concert_attendance = {user.id: user.get_number_of_preferences() for user in network.users}
    sorted_users_by_concerts = sorted(user_concert_attendance, key=user_concert_attendance.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_concerts) * 12 // 100)
    top_12_percent_users = sorted_users_by_concerts[:top_12_percent_count]

    return top_12_percent_users

def strategy_friends_with_most_concert_interests():
    network = fill_network()

    friend_concert_interests = {}
    for user in network.users:
        total_interests = 0
        for friend in network.get_friends_of(user.id):
            total_interests += friend.get_number_of_preferences()
        friend_concert_interests[user.id] = total_interests

    sorted_users_by_friends_concert_interest = sorted(friend_concert_interests, key=friend_concert_interests.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_friends_concert_interest) * 12 // 100)
    top_12_percent_users = sorted_users_by_friends_concert_interest[:top_12_percent_count]

    return top_12_percent_users

def strategy_most_friends_with_common_preferences():
    network = fill_network()

    shared_preferences_count = {}
    for user in network.users:
        shared_count = 0
        user_prefs = set(key for key, value in user.preferences.items() if value == 1)
        for friend in network.get_friends_of(user.id):
            friend_prefs = set(key for key, value in friend.preferences.items() if value == 1)
            shared = user_prefs.intersection(friend_prefs)
            shared_count += len(shared)
        shared_preferences_count[user.id] = shared_count

    sorted_users_by_shared_prefs = sorted(shared_preferences_count, key=shared_preferences_count.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_shared_prefs) * 12 // 100)
    top_12_percent_users = sorted_users_by_shared_prefs[:top_12_percent_count]

    return top_12_percent_users

def strategy_most_friends_with_common_preferences_with_concert_prob():
    network = fill_network()

    shared_preferences_count = {}
    for user in network.users:
        shared_weighted = 0
        user_prefs = set(key for key, value in user.preferences.items() if value == 1)
        for friend in network.get_friends_of(user.id):
            friend_prefs = set(key for key, value in friend.preferences.items() if value == 1)
            shared = user_prefs.intersection(friend_prefs)
            shared_weighted_count = sum(concert_prob_per_day.get(pref) for pref in shared)  # weighing by probabilities
            shared_weighted += shared_weighted_count
        shared_preferences_count[user.id] = shared_weighted

    sorted_users_by_shared_prefs = sorted(shared_preferences_count, key=shared_preferences_count.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_shared_prefs) * 12 // 100)
    top_12_percent_users = sorted_users_by_shared_prefs[:top_12_percent_count]

    return top_12_percent_users


def avg_and_plot(data):
    # Get the individual classes
    infected = np.array([run['infected'] for run in data])
    dead = np.array([run['dead'] for run in data])
    immune = np.array([run['immune'] for run in data])

    # Calculate mean and std for the individual classes
    infected_mean = np.mean(infected, axis=0)
    infected_err = np.std(infected, axis=0)

    dead_mean = np.mean(dead, axis=0)
    dead_err = np.std(dead, axis=0)

    immune_mean = np.mean(immune, axis=0)
    immune_err = np.std(immune, axis=0)

    # Get the time coordinate
    t = np.linspace(0, len(infected_mean), len(infected_mean))

    # Plot each class with the error bars
    plt.figure(figsize=(14, 8))

    plt.plot(t, infected_mean, label="infected", c="orange")
    plt.errorbar(t, infected_mean, yerr=infected_err, capsize=3, fmt=" ", c="orange")

    plt.plot(t, dead_mean, label="dead", c="red")
    plt.errorbar(t, dead_mean, yerr=dead_err, capsize=3, fmt=" ", c="red")

    plt.plot(t, immune_mean, label="immune", c="blue")
    plt.errorbar(t, immune_mean, yerr=immune_err, capsize=3, fmt=" ", c="blue")

    plt.legend()
    plt.show()

def try_strategy(ids, average_number=1):
    all_results = []
    for i in range(average_number):
        print("LOAD DATA:")
        friendships = load_friendships()
        preferences = load_preferences()

        G = build_social_graph(friendships)
        add_preferences_to_graph(G, preferences)
        print("SIMULATING:")

        result = simulate_epidemic(G, ids, concert_prob_per_day, attendence_prob, days=200, initial_infected=81)
        all_results.append(result)

    # Print results
    #print_daily_results(results)
    #plot_epidemic_curves(all_results, '', save_to_file=False)

    for result in all_results:
        print(result['dead'][len(result['dead']) - 1])
    average_last_dead = np.mean([result['dead'][-1] for result in all_results])
    print("Average of last entries of dead:", average_last_dead)

    avg_and_plot(all_results)

#try_strategy(strategy_no_vaccination(), average_number=10)
try_strategy(strategy_random_vaccination(), average_number=20)
#try_strategy(strategy_most_friends(), average_number=10)
#try_strategy(strategy_most_genres_interested(), average_number=10)
#try_strategy(strategy_friends_with_most_concert_interests(), average_number=10)
try_strategy(strategy_most_friends_with_common_preferences(), average_number=20)
try_strategy(strategy_most_friends_with_common_preferences_with_concert_prob(), average_number=20)





