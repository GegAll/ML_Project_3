import random

def simulate_epidemic(
    G, vaccine_candidates, concert_prob, attendence_prob, days=14, initial_infected=10
):
    """
    Simulates an epidemic over a number of days with 100% mortality rate and tracks healthy individuals.

    Args:
        G (nx.Graph): Social graph.
        vaccine_candidates (list): List of IDs of vaccinated individuals.
        concert_prob (dict): Probability of a concert happening per genre.
        attendence_prob (dict): Probability of friends attending concerts based on preferences.
        days (int): Number of days to simulate. Default is 14.
        initial_infected (int): Number of individuals to start as infected.

    Returns:
        dict: Dictionary tracking daily outcomes (infected, dead, healthy).
    """
    # Initialize node attributes
    for node in G.nodes():
        G.nodes[node]['status'] = 'susceptible'  # All nodes start susceptible
        G.nodes[node]['days_infected'] = 0

    # Vaccinate the proposed candidates
    for candidate in vaccine_candidates:
        if candidate in G:
            G.nodes[candidate]['status'] = 'vaccinated'

    # Randomly infect initial individuals
    all_nodes = [node for node in G.nodes if G.nodes[node]['status'] == 'susceptible']
    initial_infected_nodes = random.sample(all_nodes, min(initial_infected, len(all_nodes)))
    for node in initial_infected_nodes:
        G.nodes[node]['status'] = 'infected'

    # Track daily results
    results = {
        'day': [],
        'infected': [],
        'dead': [],
        'healthy': []
    }

    for day in range(days):
        daily_infected = []

        # Simulate daily concert attendance
        for genre, prob in concert_prob.items():
            if random.random() < prob:
                # Identify attendees for today's concert
                attendees = [
                    node for node in G.nodes()
                    if G.nodes[node]['status'] in ['susceptible', 'infected']
                    and G.nodes[node]['preferences'].get(genre, 0) == 1
                ]

                # Simulate virus spread among attendees
                for node1 in attendees:
                    if G.nodes[node1]['status'] == 'infected':
                        for node2 in attendees:
                            if (
                                G.has_edge(node1, node2) and
                                G.nodes[node2]['status'] == 'susceptible'
                            ):
                                id1_likes = G.nodes[node1]['preferences'][genre] == 1
                                id2_likes = G.nodes[node2]['preferences'][genre] == 1
                                if random.random() < attendence_prob[(id1_likes, id2_likes)]:
                                    daily_infected.append(node2)
                                    G.nodes[node2]['status'] = 'infected'

        # Update statuses of infected nodes
        for node in G.nodes():
            if G.nodes[node]['status'] == 'infected':
                G.nodes[node]['days_infected'] += 1
                if G.nodes[node]['days_infected'] == 14:  # End of infection period
                    G.nodes[node]['status'] = 'dead'

        # Record daily outcomes
        healthy_count = len([
            n for n in G.nodes
            if G.nodes[n]['status'] in ['susceptible', 'vaccinated']
        ])
        results['day'].append(day + 1)
        results['infected'].append(len([n for n in G.nodes if G.nodes[n]['status'] == 'infected']))
        results['dead'].append(len([n for n in G.nodes if G.nodes[n]['status'] == 'dead']))
        results['healthy'].append(healthy_count)

    return results
