import csv

universities = []

with open('data/universities.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        universities.append(row)

def findUniversityLink(uni: str):
    uni = uni.lower()
    for univ in universities:
        univName = univ[0].lower()
        if univName.startswith(uni) or univName.find(uni) > -1:
            return univ[1]
    return -1