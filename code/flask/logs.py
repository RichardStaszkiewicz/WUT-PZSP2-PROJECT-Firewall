def get_logs():
    with open("./logs/events.log", 'r') as log_file:
        log_string = log_file.read()
    response = log_string.split("DEBUG")

    return response
