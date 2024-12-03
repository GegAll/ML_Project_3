from infrastucture import importer
from infrastucture.user import User


class Network:
    """
    This class represents a social network where users can be added and their relationships
    managed.

    Users can be added to the network, and friendships (relationships) can be formed between
    users. The class supports querying for users and their friends.

    :ivar genres: List of music genres associated with the network (in order).
    :ivar users: List of users in the network.
    """
    genres: list[str] = [
        "Classical",
        "Folk",
        "Jazz Hip Hop",
        "Electro Pop/Electro Rock",
        "Dancefloor",
        "Indie Rock/Rock pop",
        "Singer & Songwriter",
        "Comedy",
        "Musicals",
        "Chill Out/Trip-Hop/Lounge",
        "Soundtracks",
        "Disco",
        "Old school soul",
        "Rock",
        "Romantic",
        "Bluegrass",
        "Indie Rock",
        "Contemporary Soul",
        "Blues",
        "Old School",
        "Baroque",
        "Instrumental jazz",
        "Urban Cowboy",
        "Asian Music",
        "Tropical",
        "Early Music",
        "Classic Blues",
        "Indie Pop",
        "Bolero",
        "Spirituality & Religion",
        "Dancehall/Ragga",
        "Dance",
        "R&B",
        "Pop",
        "Film Scores",
        "Grime",
        "Electro Hip Hop",
        "Metal",
        "West Coast",
        "Acoustic Blues",
        "Indie Pop/Folk",
        "International Pop",
        "Sports",
        "Trance",
        "Ska",
        "Brazilian Music",
        "Bollywood",
        "Nursery Rhymes",
        "Alternative Country",
        "Indian Music",
        "TV shows & movies",
        "Dubstep",
        "Classical Period",
        "Chicago Blues",
        "Vocal jazz",
        "TV Soundtracks",
        "Latin Music",
        "Rock & Roll/Rockabilly",
        "Delta Blues",
        "African Music",
        "Opera",
        "Ranchera",
        "Oldschool R&B",
        "Kids & Family",
        "Modern",
        "Soul & Funk",
        "Electro",
        "Alternative",
        "Dub",
        "Electric Blues",
        "Rap/Hip Hop",
        "Techno/House",
        "Country Blues",
        "Traditional Country",
        "Country",
        "East Coast",
        "Contemporary R&B",
        "Jazz",
        "Game Scores",
        "Films/Games",
        "Reggae",
        "Hard Rock",
        "Kids",
        "Dirty South"
    ]

    def __init__(self):
        self.users: list[User] = []

    def add_user(self, id):
        """
        Adds a new user to the list of users.
        Only use in fill_network() as list needs to be ordered for get_user_by_id()

        :param id: The integer ID for the new user.
        :return: The newly created `User` object.
        """
        newUser = User(id)
        self.users.append(newUser)
        return newUser

    def add_relationship(self, id1, id2):
        """
        Establish a bi-directional friendship relationship between two users.
        This method fetches the users by their IDs and adds each user to the other's
        friend list. If either user is not found or if both IDs are the same, the method
        returns without making any changes.

        :param id1: The ID of the first user.
        :param id2: The ID of the second user.
        """
        if id1 == id2: return

        user1 = self.get_user_by_id(id1)
        user2 = self.get_user_by_id(id2)

        if user1 is None or user2 is None: return

        user1.add_friend(user2)
        user2.add_friend(user1)

    def get_user_by_id(self, id):
        """
        Retrieves a user from the users dictionary by their ID.
        The users list is ordered to increase performance.
        If the user is found and the ID matches the given ID, the user is
        returned. If no matching user is found, the function returns None.

        :param id: The unique identifier of the user to retrieve.
        :return: The user object if found, otherwise None.
        """
        user = self.users[id]
        if user.id == id: return user
        return None

    def get_friends_of(self, id):
        """
        Retrieve the list of friends for a user by their ID.

        :param id: The unique identifier of the user
        :return: A list of friends for the user or an empty list if user does not exist
        """
        user = self.get_user_by_id(id)
        if user is None: return None
        return user.friends


def fill_network():
    """
    Create a user network and populate it with users and their relationships.

    This function initializes an instance of the Network class, adds users with
    IDs ranging from 0 to 8310, and imports user relationships from a CSV file.
    It then adds the relationships to the network.

    :return: An instance of Network populated with users and their relationships.
    """
    # Create network
    network = Network()

    # Add all users
    for i in range(0, 8311):
        network.add_user(i)
    print("Loaded all users")

    # Import relations between users
    relations = importer.read_friends_file("grupee_data/friends.csv")
    for relation in relations:
        network.add_relationship(relation[0], relation[1])
    print("Loaded all relations")

    return network
