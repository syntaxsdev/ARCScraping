import csv

universities = []
tlds = [
    ".edu",
    ".ac",
    ".ac.at",
    ".ac.cn",
    ".ac.cr",
    ".ac.id",
    ".ac.il",
    ".ac.in",
    ".ac.ir",
    ".ac.jp",
    ".ac.ke",
    ".ac.kr",
    ".ac.nz",
    ".ac.ru",
    ".ac.th",
    ".ac.uk",
    ".ac.za",
    ".edu.au",
    ".edu.cn",
    ".edu.co",
    ".edu.my",
    ".edu.ph",
    ".edu.sg",
    ".edu.tr",
    ".edu.tw",
    ".edu.uy",
    ".edu.vn",
    ".ieee.org"
]

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


def findTLD(uni: str):
    if any(tld in uni for tld in tlds):
        return 1
    return -1