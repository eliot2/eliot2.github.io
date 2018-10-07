#!/usr/bin/env python
import sys
import csv
import webbrowser


#this program assumes that the csv is ordered by student id (key)
#given the .csv as file 1, and the output new .csv as file 2, 
#this script will convert the cohort into the final format .csv
#where each line is a single student and their history through the school
#NOTE: both called files must be in the same directory, though you
#COULD write the code yourself to parse the directories,
#it's easier if you do: python termParser.py someCohort.csv newCohort.csv


strBuffer = []
levelBuffer = ""
outString = ""
numFrTerms = 0
numSpTerms = 0
numJuTerms = 0
numSrTerms = 0
sameLevelTerm = False

anchorKey = ""
currentKey = ""

#column numbers ---
keyColumn = 0
termColumn = 1
yearColumn = 2
levelColumn = 3
inStateColumn = 4
isFemaleColumn = 5
ethnicityColumn = 6
ageColumn = 7
majorColumn = 8
gpaStartColumn = 9
gpaPostColumn = 10
rowNum = 0
isFemale = 0

isTimeTraveler = False

gpaString = ""

inFile  = open("2010SpecificCohort.csv", "r")
csvIN = csv.reader(inFile, delimiter=',', quotechar='"')
outFile = open("FINAL.csv", "w")
csvOUT  = csv.writer(outFile,delimiter=',', quotechar='"', doublequote=False, quoting=csv.QUOTE_ALL)
outFile.write("Fa/Sp_Year,StartMajor,F1,F2,F+,P1,P2,P+,J1,J2,J+,S1,S2,S+,isFem,StartAge,Ethnicity,StartGPA,gF1,gF2,gF+,gP1,gP2,gP+,gJ1,gJ2,gJ+,gS1,gS2,gS+,StudentKey\n") 

navigate = True
while navigate:
    navigate = False
    csvFile = csv.reader(inFile, delimiter=',', quotechar='"', doublequote=False)
    for row in csvFile:
        
        rowNum += 1
        #set current key equal to the student ID in the row
        currentKey = row[0]
        #test case for first iteration included
        if anchorKey == "":
            anchorKey = row[0]
            strBuffer.append(row)
        else:
            if currentKey == anchorKey:
                #string buffer contains all the rows of the same student
                strBuffer.append(row)
            else:
                firstRow = strBuffer[0]
                firstYear = str(firstRow[yearColumn])
                firstTerm = str(firstRow[termColumn])
                isFemale = str(firstRow[isFemaleColumn])
                gpaString = str(firstRow[gpaStartColumn])
                studentKey = str(firstRow[keyColumn])

                cohort = firstTerm[:2]+firstYear

                startingMajor = firstRow[majorColumn]

                studentLine = cohort+","+startingMajor
                
                frCount = 0 #these count # of semesters being that level
                spCount = 0
                juCount = 0
                srCount = 0
                '''Gets counted elsewhere, but saved for possible future use
                for rowTerm in range(0, len(strBugger)):
                    if "Freshman" == strBuffer[rowTerm][levelColumn]:
                        frCount += 1
                    if "Sophomore" == strBuffer[rowTerm][levelColumn]:
                        spCount += 1
                    if "Junior" == strBuffer[rowTerm][levelColumn]:
                        juCount += 1
                    if "Senior" == strBuffer[rowTerm][levelColumn]:
                        srCount += 1
                '''
                loopCount = 0
                
                gpaTotal = 0.0
                gpaCount = 0.0
                #for each row of a student
                for rowTerm in range(0, len(strBuffer)):
                    #are you fr?
                    isFresh = ("Freshman" == strBuffer[rowTerm][levelColumn])
                    
                    #if freshman, make sure they weren't a sophomore/junior/senior in the past
                    if isFresh:
                        for termDate in range(rowTerm, 0, -1):
                            if "Junior" == strBuffer[termDate-1][levelColumn]:
                                isTimeTraveler = True
                            if "Senior" == strBuffer[termDate-1][levelColumn]:
                                isTimeTraveler = True
                            if "Sophomore" == strBuffer[termDate-1][levelColumn]:
                                isTimeTraveler = True
                    
                    #if fr && fr count < 2, add major
                    if (isFresh and loopCount < 2):
                        studentLine += ","+strBuffer[rowTerm][majorColumn]
                        gpaString += ","+strBuffer[rowTerm][gpaPostColumn]
                    #else if count < 2, add n/a
                    elif (loopCount < 2):
                        studentLine += ","+"n/a"
                        gpaString += ","+"0.0"
                    #if fr
                    if isFresh:
                        frCount += 1
                        gpaLen = len(strBuffer[rowTerm][gpaPostColumn])
                        gpaTotal += float(strBuffer[rowTerm][gpaPostColumn]) if gpaLen > 2 else 0.0 
                        gpaCount += 1.0
                    loopCount += 1
                
                if loopCount == 1:
                    studentLine+=","+"n/a"
                    gpaString += ","+"0.0"
                #total semesters taken gets added
                studentLine+=","+str(frCount)
                gpaString += ","+str(gpaTotal/gpaCount) if gpaCount > 0 else ","+str(0.0)
                gpaTotal = 0
                gpaCount = 0
                
                #repeat for sophomores
                '''SOPHOMORES'''
                loopCount = 0
                #for each row of a student
                for rowTerm in range(0, len(strBuffer)):
                    rowTerm += frCount
                    if(rowTerm > len(strBuffer)-1):
                        if frCount >= len(strBuffer):
                            studentLine+=",n/a,n/a"
                            gpaString+= ","+"0.0,0.0"
                        break
                    #are you sp?
                    isSoft = ("Sophomore" == strBuffer[rowTerm][levelColumn])
                    
                    #if sopohomore, make sure they weren't a junior/senior in the past
                    if isSoft:
                        for termDate in range(rowTerm, 0, -1):
                            if "Junior" == strBuffer[termDate-1][levelColumn]:
                                isTimeTraveler = True
                            if "Senior" == strBuffer[termDate-1][levelColumn]:
                                isTimeTraveler = True

                    #if sp && sp count < 2, add major
                    if (isSoft and spCount < 2):
                        studentLine += ","+strBuffer[rowTerm][majorColumn]
                        gpaString += ","+strBuffer[rowTerm][gpaPostColumn]
                    #else if count < 2, add n/a
                    elif (loopCount < 2):
                        studentLine += ","+"n/a"
                        gpaString += ","+"0.0"
                    #if sp
                    if isSoft:
                        #sp count ++
                        spCount += 1
                        gpaLen = len(strBuffer[rowTerm][gpaPostColumn])
                        gpaTotal += float(strBuffer[rowTerm][gpaPostColumn]) if gpaLen > 2 else 0.0 
                        gpaCount += 1.0
                    loopCount += 1
                
                if loopCount == 1:
                    studentLine+=","+"n/a"
                    gpaString += ","+"0.0"
                #total semesters taken gets added
                studentLine+=","+str(spCount)    
                gpaString +=  ","+str(gpaTotal/gpaCount) if gpaCount > 0 else ","+str(0.0)
                gpaTotal = 0
                gpaCount = 0
                

                '''JUNIORS CODE'''
                loopCount = 0
                #for each row of a student
                for rowTerm in range(0, len(strBuffer)):
                    rowTerm += frCount+spCount
                    if(rowTerm > len(strBuffer)-1):
                        if frCount+spCount >= len(strBuffer):
                            studentLine+=",n/a,n/a"
                            gpaString+= ","+"0.0,0.0"
                        break
                    #are you jr?
                    isJuni = ("Junior" == strBuffer[rowTerm][levelColumn])
                    
                    #if junior, make sure they weren't a senior in the past
                    if isJuni:
                        for termDate in range(rowTerm, 0, -1):
                            if "Senior" == strBuffer[termDate-1][levelColumn]:
                                isTimeTraveler = True

                    #if fr && fr count < 2, add major
                    if (isJuni and juCount < 2):
                        studentLine += ","+strBuffer[rowTerm][majorColumn]
                        gpaString += ","+strBuffer[rowTerm][gpaPostColumn]
                    #else if count < 2, add n/a
                    elif (loopCount < 2):
                        studentLine += ","+"n/a"
                        gpaString += ","+"0.0"
                    #if fr
                    if isJuni:
                        #fr count ++
                        juCount += 1
                        gpaLen = len(strBuffer[rowTerm][gpaPostColumn])
                        gpaTotal += float(strBuffer[rowTerm][gpaPostColumn]) if gpaLen > 2 else 0.0 
                        gpaCount += 1.0
                    loopCount += 1
                
                if loopCount == 1:
                    studentLine+=","+"n/a"
                    gpaString += ","+"0.0"
                #total semesters taken gets added
                studentLine+=","+str(juCount)
                gpaString +=  ","+str(gpaTotal/gpaCount) if gpaCount > 0 else ","+str(0.0)
                gpaTotal = 0
                gpaCount = 0

                
                
                '''SENIOR CODE'''
                loopCount = 0
                #for each row of a student
                for rowTerm in range(0, len(strBuffer)):
                    rowTerm += frCount+spCount+juCount
                    if(rowTerm > len(strBuffer)-1):
                        if frCount+spCount+juCount >= len(strBuffer):
                            studentLine+=",n/a,n/a"
                            gpaString+= ","+"0.0, 0.0"
                        break
                    #are you fr?
                    isSeno = ("Senior" == strBuffer[rowTerm][levelColumn])
                    
                    #if fr && fr count < 2, add major
                    if (isSeno and srCount < 2):
                        studentLine += ","+strBuffer[rowTerm][majorColumn]
                        gpaString += ","+strBuffer[rowTerm][gpaPostColumn]
                    #else if count < 2, add n/a
                    elif (loopCount < 2):
                        studentLine += ","+"n/a"
                        gpaString += ","+"0.0"
                    #if fr
                    if isSeno:
                        #fr count ++
                        srCount += 1
                        gpaLen = len(strBuffer[rowTerm][gpaPostColumn])
                        gpaTotal += float(strBuffer[rowTerm][gpaPostColumn]) if gpaLen > 2 else 0.0 
                        gpaCount += 1.0
                    loopCount += 1
                
                if loopCount == 1:
                    studentLine+=","+"n/a"
                    gpaString += ","+"0.0"
                #total semesters taken gets added
                studentLine+=","+str(srCount)
                gpaString += ","+str(gpaTotal/gpaCount) if gpaCount > 0 else ","+str(0.0)
                gpaTotal = 0
                gpaCount = 0

                
                studentLine+=","+isFemale
                studentLine+=","+firstRow[ageColumn]
                studentLine+=","+firstRow[ethnicityColumn]
                studentLine+=","+gpaString
                studentLine+=","+studentKey

                if not isTimeTraveler:
                    csvOUT.writerow(studentLine.split(','))
                isTimeTraveler = False
                #update anchor
                anchorKey = currentKey
                strBuffer = []
                strBuffer.append(row)
                isFemale = 0

inFile.close()
outFile.close()
'''
#add all to string
for x in range(0, numFrTerms):
	outString += "Fr"+str(x+1)
for x in range(0, numSpTerms):
	outString += "Sp"+str(x+1)
for x in range(0, numJuTerms):
	outString += "Ju"+str(x+1)
for x in range(0, numSrTerms):
	outString += "Sr"+str(x+1)
print outString
'''

#final new csv format:
'''
fa/sp year | Starting Major | F1 | F2 | F++ | S1 | S2 | S++ | J1 | J2 | J++ | N1 | N2 | N++
-------------------------------------------------------------------------------------------
fa 2010      CMSC            CMSC,CMSC,  0  ,CMSC,CMSC,  0  ,CMSC,CMSC,  0  ,CMSC,CMSC, 0
sp 2010      etc.
fa 2011
sp 2011
fl 2012
sp 2012
fa 2013
sp 2013 
'''
    
#something to notify us the program is finished.
webbrowser.open("https://www.youtube.com/watch?v=pmGCDVKQgyk")
