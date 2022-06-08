def get_logs():
    response = " "
    with open("./logs/events.log", 'r') as log_file:
        line = "a"
        while(line):
            line = log_file.readline()
            line.rstrip()
            response += line
    response.replace('\n', '<br />')
    return response
