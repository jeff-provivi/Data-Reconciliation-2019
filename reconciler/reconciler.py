#This script checks the raw data from the Jalisco 2019 trials against the compiled trial summary files.

#Imports (obviously, this will need to be changed)
import os
import re

class Reconciler:
    def __init__(self):
      print('init')

    def reconcile_data_files(self, inputDirectoryPath, outputPath):
      
      #Get list of all subdirectories in the Jalisco dataset
      subdirectories = next(os.walk(inputDirectoryPath))[1]

      #Check if the subdirectory names are a 2019 trial id
      trialIDs = []
      for subdirectory in subdirectories:
        if bool(re.match(re.compile("19-MX.+-WC"), subdirectory)):
          trialIDs.append(subdirectory)

      #Run the reconciliations for each trial id
      for trialID in trialIDs:
        currentTrial = trialID
        currentPath = inputDirectoryPath + trialID + '/'

        #Get filenames in the trial records
        files = next(os.walk(currentPath))[2]
        
        #Check if file names match the expected excel format
        dataFiles = []
        for fileName in files:
          if bool(re.match(re.compile("19-MX.+xlsx"), fileName)):
            dataFiles.append(fileName)

        #Check for the presence of a COMPLETO file
        hasSummary = False
        for dataFile in dataFiles:
          if bool(re.match(re.compile("19-MX.+COMPLETO.xlsx"), dataFile)):
            hasSummary = True

        if hasSummary:
          print(currentTrial + " has a COMPLETO file")
          #Add more conditionally executed checks

        else:
          print(currentTrial + " does not have a COMPLETO file")
           
          


