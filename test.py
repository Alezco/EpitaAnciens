#!/usr/bin/env python

import requests
import csv

PROMO_FIRST = 1989
PROMO_LAST = 2017
URL = 'http://www.epita-anciens.fr/annuaire/index.php?'

class Student:
    firstname = ''
    lastname = ''
    promo = 0
    business = ''
    city = ''

    def __iter__(self):
        return iter([self.firstname, self.lastname, self.promo, self.business, self.city])

students = list()

def getStudentsByPage(r):
    res = r.text
    tab = res.split('<table')[12]
    tab2 = tab.split('<!-- phpdigInclude -->')[1]
    tab3 = tab2.split('</table>')[0]

    studentsRaw = tab3.split('<tr')
    studentsRaw = studentsRaw[1:]
    for i in studentsRaw:
        student = Student()
        student.firstname = i.split('<td>')[2].replace('</td>', '').encode('utf-8')
        student.lastname = i.split('<td>')[1].replace('</td>', '').encode('utf-8')
        student.promo = i.split('<td>')[5].replace('</td>', '').encode('utf-8')
        student.business = i.split('<td>')[3].replace('</td>', '').encode('utf-8')
        student.city = i.split('<td>')[4].replace('</td>', '').encode('utf-8')
        students.append(student)

def getNbStudentsByPromo(promo):
    r = requests.post(URL, data={'nom': '%%%%', 'promo': str(promo), 'Rechercher': 'Rechercher'})
    res = r.text
    return int(res.split('<table')[10].split('sur')[1].split(')')[0])

def printStudents(students):
    for i in students:
        print(i.firstname)
        print(i.lastname)
        print(i.promo)
        print(i.business)
        print(i.city)
        print('===================================')

for promo in range(PROMO_FIRST, PROMO_LAST):
    for i in range(getNbStudentsByPromo(promo) / 20 + 1):
        r = requests.post(URL + 'start=' + str(i * 20), data={'nom': '%%%%', 'promo': str(promo), 'Rechercher':'Rechercher'})
        getStudentsByPage(r)
    print(promo)

with open('students.csv', 'wb') as csv_file:
    wr = csv.writer(csv_file, delimiter=",")
    for student in students:
        wr.writerow(list(student))
