#!/bin/bash
while inotifywait -e close_write Conf.json; do cp Conf.json New.json; done
