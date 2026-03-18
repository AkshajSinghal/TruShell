def clock_ascii_1(hour, minutes):
    template = """
     ___
    |---|
    |_|_|
    |   |
    |   |
    |   |
    |   |
    |   |
    |___|
   /_____\\
   |HH:MM|
   |_____|
   |.....|
   \ ___ /
    |   |
    |   |
    |   |
    | . |
    | . |
    | . | 
    | . |
    | . |
    | . |
    | . |
    | . |
    |___|

        """
    clock_ascii = template.replace("HH", f"{hour}")
    clock_ascii = clock_ascii.replace("MM", f"{minutes}")

    return clock_ascii
