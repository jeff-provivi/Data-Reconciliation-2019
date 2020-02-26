#This script checks the raw data from the Jalisco 2019 trials against the compiled trial summary files.

#Imports (obviously, this will need to be changed)
import os
import re
import pandas

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
      for trialID in trialIDs[0:1]:
        currentTrial = trialID
        currentPath = inputDirectoryPath + trialID + '/'

        #Get filenames in the trial records
        files = next(os.walk(currentPath))[2]
        
        #Check if file names match the expected excel format
        dataFiles = []
        for fileName in files:
          if bool(re.match(re.compile("19-MX.+xlsx"), fileName)):
            dataFiles.append(fileName)

        #Check for the presence of a COMPLETO file. If not present, print error and exit. Continue otherwise.
        hasSummary = False
        summaryFileName = ''
        for dataFile in dataFiles:
          if bool(re.match(re.compile("19-MX.+COMPLETO.xlsx"), dataFile)):
            summaryFileName = dataFile
            hasSummary = True

        if hasSummary == False:
          print(currentTrial + " does not have a COMPLETO file")

        #Continue checks for trials with summary files.
        else:
         
          #Read in the two summary sheets and begin transforming them into useful dataframes
 
          #Read in the trap data summary sheet, and transform it into a clean dataframe with trapIDs 
          #and observation dates
          summaryTrapCounts = pandas.read_excel(currentPath + summaryFileName, sheet_name=0, header=None)
          trapCounts = summaryTrapCounts.iloc[28:, 2:]
          transformedTrapCountsSummary = pandas.DataFrame(trapCounts).reset_index(drop=True)
         
          trapCountDates = summaryTrapCounts.iloc[15, 3:].copy().tolist()
          newColumnNames = ['trapID'] + trapCountDates
          transformedTrapCountsSummary.columns = newColumnNames


          #Read in the plant data summary sheet, then split the counts and damages into separate dataframes
          summaryPlantData = pandas.read_excel(currentPath + summaryFileName, sheet_name=1, header=None)
          
          daminsRowMask = [True, True, True, True] + list(summaryPlantData.iloc[18, 4:] == 'DAMINS')

          print(summaryPlantData.loc[:, daminsRowMask])



          #print(summaryPlantData.iloc[18, 4:] == 'COUNT')
           
          


