from experiment import concert_prob_per_day
from infrastucture.network import fill_network, Network
from simulation import simulate_epidemic
from vaccination import add_preferences_to_graph, attendence_prob, build_social_graph, load_friendships, \
    load_preferences, plot_epidemic_curves, print_daily_results


def strategy_no_vaccination():
    return [], fill_network()


def strategy_most_friends():
    network = fill_network()

    user_friends_count = {user: len(network.get_friends_of(user.id)) for user in network.users}
    sorted_users_by_friends = sorted(user_friends_count, key=user_friends_count.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_friends) * 12 // 100)
    top_12_percent_users = sorted_users_by_friends[:top_12_percent_count]

    return top_12_percent_users, network


def strategy_most_genres_interested():
    network = fill_network()

    user_concert_attendance = {user.id: sum(user.preferences) for user in network.users}
    sorted_users_by_concerts = sorted(user_concert_attendance, key=user_concert_attendance.get, reverse=True)
    top_12_percent_count = max(1, len(sorted_users_by_concerts) * 12 // 100)
    top_12_percent_users = sorted_users_by_concerts[:top_12_percent_count]

    return top_12_percent_users, network

def try_strategy(to_try):
    ids, network = to_try()

    print("LOAD DATA:")
    friendships = load_friendships()
    preferences = load_preferences()

    G = build_social_graph(friendships)
    add_preferences_to_graph(G, preferences)
    print("SIMULATING:")
    results = simulate_epidemic(G, ids, concert_prob_per_day, attendence_prob, days=365, initial_infected=10)

    # Print results
    print_daily_results(results)

    plot_epidemic_curves(results, '', save_to_file=False)

try_strategy(strategy_most_genres_interested)

