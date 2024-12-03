import pandas as pd
from experiment import concert_prob_per_day
import json
import networkx as nx
import random
from tqdm import tqdm
from simulation import simulate_epidemic
import matplotlib.pyplot as plt

attendence_prob = {
    #(id1 likes, id2 likes)
    (True, True): 0.393,
    (True, False): 0.018,
    (False, True): 0.018,
    (False, False): 0.002
}

def load_friendships():
    # Load of pairs of friends
    friendships = pd.read_csv("grupee_data/friends.csv", skiprows=1, names= ["id1", "id2"])

    # Drop any entries with NaN
    friendships.dropna(inplace=True)
    return friendships

def load_preferences():
    # Get preferences
    with open('grupee_data/preferences.json') as f:
        preferences = json.load(f)

    # Create a dict with {id1: {Genre1: 0, Genre2: 1, ...},
    #                    id2: {Genre2: 0, Genre2: 1, ...},
    #                     ...
    #                       }
    preferences_dict = {}
    for id in tqdm(preferences, desc='Load Preferences', leave=True):
        temp_dict = {}
        for i, genre in enumerate(concert_prob_per_day.keys()):
            temp_dict[genre] = int(preferences[id][i])

        preferences_dict[int(id)] = temp_dict

    return preferences_dict


def build_social_graph(friendships):
    G = nx.Graph()
    for _, row in tqdm(friendships.iterrows(), desc='Build Graph', leave=True):
        G.add_edge(row['id1'], row['id2'])
    return G


def add_preferences_to_graph(G, preferences):
    for node, genres in tqdm(preferences.items(), desc='Add Preferences', leave=True):
        if node in G:
            nx.set_node_attributes(G, {node: genres}, "preferences")


def compute_centralities(G):
    # Compute various centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    
    # Combine or analyze them separately
    return degree_centrality, betweenness_centrality, closeness_centrality

def simulate_concert_attendance(G, concert_prob, attendence_prob):
    infected_nodes = set()
    for genre, prob in tqdm(concert_prob.items(), desc='Simulation', leave=True):
        if random.random() < prob:
            # Identify attendees of this genre's concert
            attendees = [
                node for node, attrs in G.nodes(data=True)
                if attrs.get("preferences", {}).get(genre, 0) == 1
            ]
            
            # Simulate transmission among attendees based on friendship and attendance probabilities
            for node1 in attendees:
                for node2 in attendees:
                    if G.has_edge(node1, node2):
                        id1_likes = G.nodes[node1]['preferences'][genre] == 1
                        id2_likes = G.nodes[node2]['preferences'][genre] == 1
                        if random.random() < attendence_prob[(id1_likes, id2_likes)]:
                            infected_nodes.add(node2)
    return infected_nodes

def select_vaccine_candidates(G, centrality, percent=0.12):
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    num_to_select = int(len(G.nodes) * percent)
    return [node for node, _ in sorted_nodes[:num_to_select]]

def write_vaccine_candidates_to_file(vaccine_candidates, filename="vaccine_candidates.txt"):
    """
    Writes the list of vaccine candidate IDs to a text file, one ID per line.

    Args:
        vaccine_candidates (list): List of user IDs selected for vaccination.
        filename (str): Name of the output file. Defaults to "vaccine_candidates.txt".
    """
    try:
        with open(filename, "w") as file:
            for candidate in vaccine_candidates:
                file.write(f"{candidate}\n")
        print(f"Vaccine candidates successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def load_vaccine_candidates(filename):
    vaccine_candidates = []
    try:
        with open(filename, "r") as file:
            while True:
                candidate=file.readline()
                if not candidate:
                    break
                print(int(candidate))
                vaccine_candidates.append(int(candidate))
        print(f"Vaccine candidate successfully read from {filename}")
    except Exception as e:
        print(f"An error occured while readin the file: {e}")
    return vaccine_candidates


def plot_epidemic_curves(results, filename):
    """
    Plots the epidemic curves for infected, dead, immune, and susceptible individuals.

    Args:
        results (dict): Dictionary containing daily counts for infected, dead, immune, and susceptible.
    """
    plt.figure(figsize=(10, 6))
    
    # Plot each category
    plt.plot(results['day'], results['infected'], label="Infected", color='orange', linewidth=2)
    plt.plot(results['day'], results['dead'], label="Dead", color='red', linewidth=2)
    plt.plot(results['day'], results['immune'], label="Immune", color='green', linewidth=2)
    plt.plot(results['day'], results['susceptible'], label="Not Infected", color='blue', linewidth=2)
    
    # Add titles and labels
    plt.title("Epidemic Simulation Curves", fontsize=16)
    plt.xlabel("Days", fontsize=14)
    plt.ylabel("Number of Individuals", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Show the plot
    plt.tight_layout()
    plt.savefig(f'{filename}.png')


if __name__ == '__main__':
    # Load data
    print('LOAD DATA ...')
    friendships = load_friendships()
    preferences = load_preferences()

    # Build graph
    print('BUILD GRAPH ...')
    G = build_social_graph(friendships)
    add_preferences_to_graph(G, preferences)
    
    # Compute centrality measures
    # degree_centrality, betweenness_centrality, closeness_centrality = compute_centralities(G)

    # Select vaccine candidates
    a_vaccine_candidates = load_vaccine_candidates('a_team_7.txt')
    b_vaccine_candidates = load_vaccine_candidates('b_team_7.txt')

    # write_vaccine_candidates_to_file(vaccine_candidates)

    print('SIMUALTION ...')
    results_a = simulate_epidemic(
        G,
        a_vaccine_candidates,
        concert_prob_per_day,
        attendence_prob,
        days=365,  # Simulate for 30 days
        initial_infected=50
    )

    results_b = simulate_epidemic(
        G,
        a_vaccine_candidates,
        concert_prob_per_day,
        attendence_prob,
        days=365,  # Simulate for 30 days
        initial_infected=50
    )

    # Print results
    for day, infected, dead, immune, susceptible in zip(
        results_a['day'], results_a['infected'], results_a['dead'], results_a['immune'], results_a['susceptible']
    ):
        print(
            f"Day {day}: Infected={infected}, Dead={dead}, Immune={immune}, Not Infected={susceptible}"
        )

    # Print results
    for day, infected, dead, immune, susceptible in zip(
        results_b['day'], results_b['infected'], results_b['dead'], results_b['immune'], results_b['susceptible']
    ):
        print(
            f"Day {day}: Infected={infected}, Dead={dead}, Immune={immune}, Not Infected={susceptible}"
        )

    plot_epidemic_curves(results_a, 'a_team_7')
    plot_epidemic_curves(results_b, 'b_team_7')
