from keystrokeParser import KeystrokeParser
from keystrokeLogger import KeystrokeLogger

def test_with_substring(substring):
    parser = KeystrokeParser()
    # logger = KeystrokeLogger()
    id = parser.id_from_substring(substring)
    if id:
        avg_time = parser.get_average_time(id)
        print(f"Average time between keystrokes: {avg_time}")
        std_dev = parser.get_std_deviation(id)
        print(f"Standard deviation: {std_dev}")
        # visualize
        # print(parser.get_all_strings(id))
        # parser.visualize_keystroke_times()
    else:
        print(f"No phrase found with the keyword: {substring}")

def test_parser_methods():
    parser = KeystrokeParser()
    # Method list: check_membership, id_from_substring, get_all_strings, get_highest_keystroke_times, get_average_time, get_std_deviation
    ### Test check_membership ###
    # Expected output: True
    valid_string = "1 2 3 4 5"
    invalid_string = "invalid_string"
    # Test check_membership, id_from_substring
    res = parser.check_membership(valid_string)
    if res:
        id = parser.id_from_substring(valid_string[:3])
        assert(parser.check_membership(id) == True)
    # Test get_all_strings
    string_list = parser.get_all_strings()
    for curr_string in string_list:
        if len(curr_string) > 100:
            curr_string = curr_string[:100] + "...[truncated]"
        print(curr_string)
    # Test math functions
    highest_times = parser.get_highest_keystroke_times()
    print(f"Highest times: {highest_times}")
    avg_time = parser.get_average_time()
    print(f"Average time between keystrokes: {avg_time}")
    std_dev = parser.get_std_deviation()
    print(f"Standard deviation: {std_dev}")
    # Test visualize
    parser.visualize_keystroke_times(excludeOutliers=True)

def fooling_around():
    parser = KeystrokeParser()
    logger = KeystrokeLogger()
    string_list = parser.get_all_strings()
    for curr_string in string_list:
        if len(curr_string) > 100:
            curr_string = curr_string[:100] + "...[truncated]"
        print(curr_string)
    avg_time = parser.get_average_time()
    print(f"Average time between keystrokes: {avg_time}")
    std_dev = parser.get_std_deviation()
    print(f"Standard deviation: {std_dev}")

def main():
    # fooling_around()
    test_parser_methods()

if __name__ == "__main__":
    # parser = KeystrokeParser()
    # logger = KeystrokeLogger()
    # print(parser.check_membership("1 2 3 4 5"))
    main()