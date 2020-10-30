import csv
import os
import glob
import os.path, time
from user import User
'''
This file will take a report from zoom, and generate a list of users who attended, and the time they were in the meeting.

File name must have the .csv extension

The 'results.txt' file will be overwritten with the new information, if you want the old information make sure to save it each time.
'''

users = []

# This will get the most recent csv file that has been added
def scan_csv_files():
    csv_files = []
    for files in glob.glob("*.csv"):
        resultFile = (files, os.path.getctime(files))
        csv_files.append(resultFile)

    csv_files.sort(key=lambda tup: tup[1], reverse=True)

    correct_csv = csv_files.pop(0)

    for deleteFile in csv_files:
        os.remove(deleteFile[0])

    return correct_csv[0]

# Open up the file named report.csv
with open(scan_csv_files()) as csv_file:
    csv_reader = list(csv.reader(csv_file, delimiter=','))
    line_count = 0

    # Computes the longest name
    longestNameLength = 0
    for row in csv_reader:
        if line_count > 0:
            length = len(row[0])
            if length > longestNameLength:
                longestNameLength = length
        line_count += 1

    # Reads the CSV file and gets all the relevent information out, puts them into a user object, and adds them to the users array
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            name = row[0]
            minutes = row[2]
            length = len(name)

            spaces = " " * (longestNameLength - length)

            user = User(name, minutes, spaces)

            users.append(user)
        line_count += 1

    # Sort users by name
    users.sort(key=lambda user: user.name)
    
    # Create new txt file to output this information into
    results = open('results.txt', 'w')

    # Go through and write each users information to a new line
    for user in users:
        results.write(f'{user.name}{user.spaces} | {user.minutes} minutes\n')

    results.close()
    
