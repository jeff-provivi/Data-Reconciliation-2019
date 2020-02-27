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
      for trialID in trialIDs:
        print('\n \nTRIAL ID: ' + trialID)
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
          if bool(re.match(re.compile("19-MX.+COMPLET..xlsx"), dataFile)):
            summaryFileName = dataFile
            hasSummary = True

        if hasSummary == False:
          print(currentTrial + " does not have a COMPLETO file")

        
        #If a summary file exists, continue with the checks
        ########################################################################################## 
        ########################################################################################## 
        else:
          print('SUMMARY FILE: ' + summaryFileName)
 
          #Read in the trap data summary sheet, and transform it into a clean dataframe with trapIDs 
          #and observation dates
          ######################################################################################## 
          summaryTrapCounts = pandas.read_excel(currentPath + summaryFileName, sheet_name=0, header=None)
          trapCounts = summaryTrapCounts.iloc[28:, 2:]
          transformedTrapCountsSummary = pandas.DataFrame(trapCounts).reset_index(drop=True)
         
          trapCountDates = summaryTrapCounts.loc[summaryTrapCounts[0].str.contains('Date', na=False), 3:].iloc[0, 0:].tolist()
          newColumnNames = ['trapID'] + trapCountDates
          transformedTrapCountsSummary.columns = newColumnNames
         
          #Trim by removing any columns or rows with all NaN values
          transformedTrapCountsSummary.dropna(how='all', inplace=True)
          transformedTrapCountsSummary.dropna(how='all', axis='columns', inplace=True)

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

          #Trim by removing any columns or rows with all NaN values
          transformedDamagesSummary.dropna(how='all', inplace=True)
          transformedDamagesSummary.dropna(how='all', axis='columns', inplace=True)


          #Get a mask of which rows refer to counts, then use that to create a counts only dataframe 
          countRowMask = list(summaryPlantData.iloc[18, 4:] == 'COUNT')
          transformedPlantCountSummary = summaryPlantData.loc[28:, [False, False, True, True] + countRowMask].reset_index(drop=True)
       
          plantCountDates = summaryPlantData.iloc[15, 4:][countRowMask].tolist()
          newColumnNames = ['transectID', 'plant number'] + plantCountDates
          transformedPlantCountSummary.columns = newColumnNames

          #Trim by removing any columns or rows with all NaN values
          transformedPlantCountSummary.dropna(how='all', inplace=True)
          transformedPlantCountSummary.dropna(how='all', axis='columns', inplace=True)

         
          #Load and reconcile all the indvidual observation files against the loaded summary data 
          ######################################################################################## 
          ########################################################################################
          for dataFile in dataFiles:
            if dataFile != summaryFileName:
              print('READING FILE: ' + dataFile)

              #Read in the trap count sheet and transform it into a clean dataframe
              ######################################################################################## 
              rawTrapCounts = pandas.read_excel(currentPath + dataFile, sheet_name=0, header=None)
              slicedTrapCounts = rawTrapCounts.iloc[26:, 2:]
              transformedTrapCounts = pandas.DataFrame(slicedTrapCounts).reset_index(drop=True)

              trapCountDates = rawTrapCounts.iloc[13, 3:].tolist()
              newColumnNames = ['trapID'] + trapCountDates
              transformedTrapCounts.columns = newColumnNames

              #Trim by removing any columns or rows with all NaN values
              transformedTrapCounts.dropna(how='all', inplace=True)
              transformedTrapCounts.dropna(how='all', axis='columns', inplace=True)

              #Read in the plant data sheet, then split the counts and damages into separate dataframes
              ######################################################################################## 
              rawPlantData = pandas.read_excel(currentPath + dataFile, sheet_name=1, header=None)
            
              #Add transect labels to all rows
              transectID = None
              for index, row in rawPlantData.iterrows():
                if index > 25:
                  if not numpy.isnan(row[2]):
                    transectID = row[2]
                  elif numpy.isnan(row[2]) and not numpy.isnan(row[3]):
                    rawPlantData.iloc[index, 2] = transectID
         
              #Get a mask of which rows refer to damages, then use that to create a damage only dataframe 
              daminsRowMask = list(rawPlantData.iloc[16, 4:] == 'DAMINS')
              transformedDamages = rawPlantData.loc[26:, [False, False, True, True] + daminsRowMask].reset_index(drop=True)
       
              damagesDates = rawPlantData.iloc[13, 4:][daminsRowMask].tolist()
              newColumnNames = ['transectID', 'plant number'] + damagesDates
              transformedDamages.columns = newColumnNames

              #Trim by removing any columns or rows with all NaN values
              transformedDamages.dropna(how='all', inplace=True)
              transformedDamages.dropna(how='all', axis='columns', inplace=True)


              #Get a mask of which rows refer to counts, then use that to create a counts only dataframe 
              countRowMask = list(rawPlantData.iloc[16, 4:] == 'COUNT')
              transformedPlantCount = rawPlantData.loc[26:, [False, False, True, True] + countRowMask].reset_index(drop=True)
       
              plantCountDates = rawPlantData.iloc[13, 4:][countRowMask].tolist()
              newColumnNames = ['transectID', 'plant number'] + plantCountDates
              transformedPlantCount.columns = newColumnNames

              #Trim by removing any columns or rows with all NaN values
              transformedPlantCount.dropna(how='all', inplace=True)
              transformedPlantCount.dropna(how='all', axis='columns', inplace=True)

              #Reconcile the observation data against the summary data
              ######################################################################################## 
              ######################################################################################## 

              #Reconciling the trap counts
              ######################################################################################## 
              
              #Check that the observation dates are in the summary file
              for date in list(transformedTrapCounts.columns)[1:]:
                if not (date in list(transformedTrapCountsSummary.columns)):
                  print('ERROR: In trial ' + currentTrial + ' and in file ' + dataFile + ': date ' + date + ' not in ' + summaryFileName)

                #Check that all observations values match
                else:
                  for index, row in transformedTrapCounts.iterrows():
                    observedValue = row[date]
                    trapID = row['trapID']

                    summaryValue = list(transformedTrapCountsSummary.loc[transformedTrapCountsSummary['trapID'] == trapID, date])[0] 

                    #print('Observed: ', observedValue, ' Summary: ', summaryValue)
                    if not (observedValue == summaryValue):
                      print('ERROR: Discrepancy between ' + summaryFileName + ' and ' + dataFile + ' at trapID ' + trapID + ' and date ' + date)

              

 

