import csv


def read_friends_file(file_path):
    """
    Reads a CSV file and returns its data starting from the second line.
    Each row should contain exactly two integers separated by a comma.

    Parameters:
    - file_path: str, the path to the CSV file

    Returns:
    - List of tuples, each containing two integers from a row of the CSV file
      starting from the second line.
    """
    data = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the first line (header)
        for row in csvreader:
            if len(row) == 2:  # Ensure each row contains exactly two elements
                int_pair = (int(row[0]), int(row[1]))  # Convert each element to an integer and make a tuple
                data.append(int_pair)
            else:
                raise ValueError(f"Row does not contain exactly two elements: {row}")
    return data
