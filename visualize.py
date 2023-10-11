import matplotlib.pyplot as plt

# Sample data
keystrokes = [
    ["a", 0.1],
    ["b", 0.2],
    ["a", 0.3],
    ["c", 0.15],
    ["b", 0.25],
    ["a", 0.2]
]
def plot_keystroke_times(keystrokes):
    """
    Plots the average keystroke time for each character based on the provided keystrokes.

    Args:
        keystrokes (list): A list of keystrokes, where each keystroke is represented by a list containing a character and a time.

    Returns:
        None
    """

    # Calculate average keystroke time for each character
    character_times = {}
    character_counts = {}
    for key, time in keystrokes:
        if key in character_times:
            character_times[key] += time
            character_counts[key] += 1
        else:
            character_times[key] = time
            character_counts[key] = 1

    for key in character_times:
        character_times[key] /= character_counts[key]

    # Plotting
    characters = list(character_times.keys())
    times = list(character_times.values())

    plt.bar(characters, times)
    plt.xlabel('Characters')
    plt.ylabel('Average Keystroke Time')
    plt.title('Average Keystroke Time for Each Character')
    plt.show()

def main():
    plot_keystroke_times(keystrokes)

if __name__ == "__main__":
    main()