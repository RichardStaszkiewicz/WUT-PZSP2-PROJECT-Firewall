# Modules

## Fire

|  Feature    | Description |
|:-----------:|:----------:|
|  Fetch      | Gets packeges and renders it into the whole messages |
|  Analyse    | Verifies the message via the rules |
|  Reject     | Sends ICMP to the sender with error code |
|  Accept     | Passes the packeges of the message forward |

## Conf

| Feature     | Description |
|:-----------:|:----------:|
| Model       | Data storage providing server with info, writing the .conf file |
| View        | Presents a data to user (IFace), recieves the control signals |
| Controller  | Interpret a signals of user, makes changes to model |

# Used Libraries

| Library    | Description |
|:----------:|:-----------:|
| inotify-tools | Listener used for uploading .conf file from Conf module to Fire |
| json       | Converts rules into json data type which is used by frontend |
| namedtuple | Used to accept any incoming data type |

# Documentation

## Buisness
The buisness documentation is in the repository under direcotory doc/

## Code
The code documentation is rendered via Doxygen plugin.
run with `doxygen pythonDox`
https://www.doxygen.nl/manual/docblocks.html
https://www.doxygen.nl/manual/docblocks.html#pythonblocks
