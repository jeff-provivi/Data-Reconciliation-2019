#This script checks the raw data from the Jalisco 2019 trials against the compiled trial summary files.

#Imports (obviously, this will need to be changed)
import os
import re
import pandas
import numpy

class Reconciler:
    def __init__(self):
      print('init')

    def reconcile_data_files(self, inputDirectoryPath, outputPath):
     
      #Define trial ids present in the data
      ############################################################################################ 
      #Get list of all subdirectories in the Jalisco dataset
      subdirectories = next(os.walk(inputDirectoryPath))[1]

      #Check if the subdirectory names are a 2019 trial id
      trialIDs = []
      for subdirectory in subdirectories:
        if bool(re.match(re.compile("19-MX.+-WC"), subdirectory)):
          trialIDs.append(subdirectory)


      #Run the reconciliations for each trial id
      ############################################################################################ 
      ############################################################################################ 
      for trialID in trialIDs[0:1]:
        currentTrial = trialID
        currentPath = inputDirectoryPath + trialID + '/'

        #Check files in each trial. If no summary file, throw an error and move to next trial
        ########################################################################################## 
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

        
        #If a summary file exists, continue with the checks
        ########################################################################################## 
        ########################################################################################## 
        else:
 
          #Read in the trap data summary sheet, and transform it into a clean dataframe with trapIDs 
          #and observation dates
          ######################################################################################## 
          summaryTrapCounts = pandas.read_excel(currentPath + summaryFileName, sheet_name=0, header=None)
          trapCounts = summaryTrapCounts.iloc[28:, 2:]
          transformedTrapCountsSummary = pandas.DataFrame(trapCounts).reset_index(drop=True)
         
          trapCountDates = summaryTrapCounts.iloc[15, 3:].copy().tolist()
          newColumnNames = ['trapID'] + trapCountDates
          transformedTrapCountsSummary.columns = newColumnNames

          #Read in the plant data summary sheet, then split the counts and damages into separate dataframes
          ######################################################################################## 
          summaryPlantData = pandas.read_excel(currentPath + summaryFileName, sheet_name=1, header=None)
            
          #Add transect labels to all rows
          transectID = None
          for index, row in summaryPlantData.iterrows():
            if index > 27:
              if not numpy.isnan(row[2]):
                transectID = row[2]
              elif numpy.isnan(row[2]) and not numpy.isnan(row[3]):
                row[2] = transectID
         
          #Get a mask of which rows refer to damages, then use that to create a damage only dataframe 
          daminsRowMask = list(summaryPlantData.iloc[18, 4:] == 'DAMINS')
          transformedDamagesSummary = summaryPlantData.loc[28:, [False, False, True, True] + daminsRowMask].reset_index(drop=True)
       
          damagesDates = summaryPlantData.iloc[15, 4:][daminsRowMask].tolist()
          newColumnNames = ['transectID', 'plant number'] + damagesDates
          transformedDamagesSummary.columns = newColumnNames

          #Get a mask of which rows refer to counts, then use that to create a counts only dataframe 
          countRowMask = list(summaryPlantData.iloc[18, 4:] == 'COUNT')
          transformedPlantCountSummary = summaryPlantData.loc[28:, [False, False, True, True] + countRowMask].reset_index(drop=True)
       
          plantCountDates = summaryPlantData.iloc[15, 4:][countRowMask].tolist()
          newColumnNames = ['transectID', 'plant number'] + plantCountDates
          transformedPlantCountSummary.columns = newColumnNames

          
          #Load and reconcile all the indvidual observation files against the loaded summary data 
          ######################################################################################## 
          ########################################################################################
          for dataFile in dataFiles[0:1]:
            if dataFile != summaryFileName:

              #Read in the trap count sheet and transform it into a clean dataframe
              ######################################################################################## 
              rawTrapCounts = pandas.read_excel(currentPath + dataFile, sheet_name=0, header=None)
              slicedTrapCounts = rawTrapCounts.iloc[26:, 2:]
              transformedTrapCounts = pandas.DataFrame(slicedTrapCounts).reset_index(drop=True)

              trapCountDates = rawTrapCounts.iloc[13, 3:].tolist()
              newColumnNames = ['trapID'] + trapCountDates
              transformedTrapCounts.columns = newColumnNames

              #Read in the plant data sheet, then split the counts and damages into separate dataframes
              ######################################################################################## 
              rawPlantData = pandas.read_excel(currentPath + dataFile, sheet_name=1, header=None)
              print(rawPlantData.iloc[26: , 2:])
            
              #Add transect labels to all rows
              observationTransectID = None
              for index, row in rawPlantData.iterrows():
                if index > 25:
                  if not numpy.isnan(row[2]):
                    observationTransectID = row[2]
                  elif numpy.isnan(row[2]) and not numpy.isnan(row[3]):
                    row[2] = observationTransectID
                print(row[2], row[3])
              print(rawPlantData.iloc[26: , 2:])
         
              #Get a mask of which rows refer to damages, then use that to create a damage only dataframe 
              daminsRowMask = list(rawPlantData.iloc[16, 4:] == 'DAMINS')
              transformedDamages = rawPlantData.loc[26:, [False, False, True, True] + daminsRowMask].reset_index(drop=True)
       
              damagesDates = rawPlantData.iloc[13, 4:][daminsRowMask].tolist()
              newColumnNames = ['transectID', 'plant number'] + damagesDates
              transformedDamages.columns = newColumnNames
              print(transformedDamages)

              #Get a mask of which rows refer to counts, then use that to create a counts only dataframe 
              #countRowMask = list(summaryPlantData.iloc[18, 4:] == 'COUNT')
              #transformedPlantCountSummary = summaryPlantData.loc[28:, [False, False, True, True] + countRowMask].reset_index(drop=True)
       
              #plantCountDates = summaryPlantData.iloc[15, 4:][countRowMask].tolist()
              #newColumnNames = ['transectID', 'plant number'] + plantCountDates
              #transformedPlantCountSummary.columns = newColumnNames

             
 

