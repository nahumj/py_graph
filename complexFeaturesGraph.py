# https://bespokeblog.wordpress.com/2011/07/07/basic-data-plotting-with-matplotlib-part-2-lines-points-formatting/

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.backends.backend_pdf import PdfPages

####
#
# ReadDataFile(FileName,DataFields,Separator=' ',SkipRows=0)
#   Reads in a file, splits its contents into columns and loads the columns into a Map.
#   
#   FileName = Name of file
#   Separator = char in file used to separate columns
#   SkipRows = number of rows to skip at head of file
#   DataFields = names of columns
#
#   Return: dictonary of columns labled with the names in DataFields
#
#   If there are less DataFields then columns in the file,
#   then extra columns will be ignored.
#   Empty lines in the file will be ignored.
#
####

def ReadDataFile(FileName,DataFields,Separator=' ',SkipRows=0):
  File = open(FileName)                                       # open the file
  
  data = {}                                                   # makes a dictonary called data
  for name in DataFields:
    data[name] = []                                           # addes an blank entry into data for each name in DataFields

  for line in File:                                           # for each line in the file...
    row = line.split(Separator)                               #  makes row, a list with the values of each column for this row

    if (len(row) >= len(DataFields)) & (SkipRows < 1):        #  if there is enough data in this row and we are not still skipping rows...
      for i in range(len(DataFields)):                        #   then for each element in DataFields...
        data[DataFields[i]].append(float(row[i]))             #   add the value from the to the correct entry in data 

    else :                                                    #  else
      if (len(row) > 0) & (SkipRows < 1):                     #   if there is not enough data in the row and we have skipped enough rows
        print (row)
        print ('error in %s... not enough columns' % FileName) # report and error in the file
        exit()
      SkipRows = SkipRows - 1                                 # if we have not skipped enough rows, decrement SkipRows

  return data

####
#
# WriteDataFile(FileName, Data, DataFields, Separator=' ', FormatStyle='columns', PrintHeader='short')
#   Writes data to FileName
#   Data for each feature will be written either in rows or columns
#   Data will be separated by the value in Separator.
#   
#   PrintHeader='short','tall','off'
####

def WriteDataFile(FileName, Data, DataFields, Separator=' ', FormatStyle='columns', PrintHeader='off', Title=''):
  
  # check to make sure all data is the same size
  sizeCheck = len(Data[DataFields[0]])
  for name in DataFields:
    if len(Data[name]) != sizeCheck:
      print('In WriteDataFile: Not all data has the same number of elements')
      exit()
  
  File = open(FileName,'w')                                       # open the file
  
  if(Title!=''):
    File.write(Title+'\n\n')
  
  if(PrintHeader=='short'):
    for nameIndex in range(len(DataFields)):
      File.write(DataFields[nameIndex])
      if (nameIndex < len(DataFields)-1):
        File.write(Separator)
    File.write('\n')
    File.write('\n')

  if(PrintHeader=='tall'):
    for nameIndex in range(len(DataFields)):
      File.write(str(nameIndex+1)+'. '+DataFields[nameIndex])
      File.write('\n')
    File.write('\n')

  if (FormatStyle=='columns'):
    for row in range(len(Data[DataFields[0]])):
      for nameIndex in range(len(DataFields)):
        File.write(Data[DataFields[nameIndex]][row])
        if (nameIndex < len(DataFields)-1):
          File.write(Separator)  
      File.write('\n')

  if (FormatStyle=='rows'):
    for name in DataFields:
      for index in range(len(Data[DataFields[0]])):
        File.write(Data[name][index])
        if (index < len(Data)-1):
          File.write(Separator) 
      File.write('\n')

  File.close()
      
      
    
      



####
#
# BuildMultiPlot(DataMap,NamesList,XCoordinateName='',Columns=1)
#   Builds a Figure with rows = # elements in Names list.
#   Each row contains a graph generated from DataMap[NamesList[row#]]
#
#   DataMap : a map with data (all entires must have the same number of elements)
#   NamesList : list of names of elements from data to be graphed
#   XCoordinateName : If specified, this element from the DataMap will determin the XCoordinate scale
#   Columns : spread the graphs over this many columns, if not defined, there will be 1 column
#             # of rows is calcualted by the number of columns and the number of elements in NamesList
#
#   Return: the figure created
#
####

def BuildMultiPlot(DataMap,NamesList,XCoordinateName='',Columns=1):
  #fig, axes = plt.subplots(nrows=len(NamesList), ncols=1, figsize=(6, 3*len(NamesList)))
  plt.figure()                                                # create a new figure

  Rows = math.ceil(float(len(NamesList))/float(Columns))      # calcualate how many rows we need
  
  if (XCoordinateName==''):                                   # if there is no XCoordinateName
    for count in range(len(NamesList)):                       # for each name
      plt.subplot(Rows,Columns,count+1)                       # go to the count-th row of in our figure (with len(NamesList) rows)
      plt.plot(DataMap[NamesList[count]],label=NamesList[count])
                                                              # plot the data for each element in name in it's own plot
      plt.title(NamesList[count], fontsize=12) 	              # set the title for this plot

  else:                                                       # else, there is a XCoordinateName
    for count in range(len(NamesList)):                       # for each name
      plt.subplot(Rows,Columns,count+1)                       # go to the count-th row of in our figure (with len(NamesList) rows)
      plt.plot(DataMap[XCoordinateName],DataMap[NamesList[count]],label=NamesList[count])
                                                              # plot the data for each element in name in it's own plot
      plt.title(NamesList[count], fontsize=12)                # set the title for this plot

  return plt.gcf()                                            # gcf = get current figure - return that.

####
#
# BuildPlot(DataMap,NamesList,XCoordinateName='',AddLegend="")
#   Builds a figure with a single plot graphing the elements from DataMap named by NamesList.
#   Axis are labled if possible, and a legend is added.
#
#   DataMap : a map with data (all entires must have the same number of elements)
#   NamesList : list of names of elements from data to be graphed
#   XCoordinateName : If specified, this element from the DataMap will determin the XCoordinate scale
#   AddLegend : if defined, places a legend ('upper left','upper right','lower left','lower right')
#
#   Return: the figure created
#
####

def BuildPlot(DataMap,NamesList,XCoordinateName='',AddLegend=''):
  plt.figure()                                                # create a new figure

  if XCoordinateName=='':                                     # if there is no XCoordinateName
    for count in range(len(NamesList)):                       # for each name
      plt.plot(DataMap[NamesList[count]],label=NamesList[count])
                                                              # plot the data for each element in name in it's own plot

  else:                                                       # else, there is a XCoordinateName
    for count in range(len(NamesList)):                       # for each name
      plt.plot(DataMap[XCoordinateName],DataMap[NamesList[count]],label=NamesList[count])
                                                              # plot the data for each element in name in it's own plot
      plt.xlabel(XCoordinateName)                             # add a X axis label

  if (AddLegend!=""):
    plt.legend(loc=AddLegend, shadow=True)                    # add a legend
    
  return plt.gcf()                                            # gcf = get current figure - return that.

	  
######## LOAD DATA

ALLRepMin = 36
ALLRepMax = 40
EQURepMin = 136
EQURepMax = 140

# make some containers
ALLaveData = []
ALLcountData = []
ALLtaskData = []

EQUaveData = []
EQUcountData = []
EQUtaskData = []

# read in the data for all reps
for rep in range(ALLRepMin,ALLRepMax+1):
  ALLaveData.append(ReadDataFile('results/all_rewarded/'+str(rep)+'/data/average.dat', ['update','merit'], Separator=' ', SkipRows=19))
  ALLcountData.append(ReadDataFile('results/all_rewarded/'+str(rep)+'/data/count.dat', ['update','num_ints', 'org_count'], Separator=' ', SkipRows=19))
  ALLtaskData.append(ReadDataFile('results/all_rewarded/'+str(rep)+'/data/tasks.dat', ['update','Not','Nand','And','OrNot','Or','AndNot','Nor','Xor','Equals'], Separator=' ', SkipRows=15))

for rep in range(EQURepMin,EQURepMax+1):
  EQUaveData.append(ReadDataFile('results/equ_rewarded/'+str(rep)+'/data/average.dat', ['update','merit'], Separator=' ', SkipRows=19))
  EQUcountData.append(ReadDataFile('results/equ_rewarded/'+str(rep)+'/data/count.dat', ['update','num_ints', 'org_count'], Separator=' ', SkipRows=19))
  EQUtaskData.append(ReadDataFile('results/equ_rewarded/'+str(rep)+'/data/tasks.dat', ['update','Not','Nand','And','OrNot','Or','AndNot','Nor','Xor','Equals'], Separator=' ', SkipRows=15))


BuildPlot(DataMap = ALLtaskData[0], NamesList = ['Not','Nand','And','OrNot','Or','AndNot','Nor','Xor','Equals'],XCoordinateName = 'update',AddLegend='lower right')
BuildPlot(DataMap = EQUtaskData[0], NamesList = ['Not','Nand','And','OrNot','Or','AndNot','Nor','Xor','Equals'],XCoordinateName = 'update',AddLegend='lower right')




###########################
# calculate the mean and standard devation for merit, male display and female display
###########################

# make containers
ALLcollectedMerits = []
EQUcollectedMerits = []

# collect the datas into one list
for rep in ALLaveData:
  ALLcollectedMerits.append(rep['merit'])
for rep in EQUaveData:
  EQUcollectedMerits.append(rep['merit'])

# get mean and Std
ALLMeritsMean = np.mean(ALLcollectedMerits, axis=0)
ALLMeritsStd = np.std(ALLcollectedMerits, axis=0)

EQUMeritsMean = np.mean(EQUcollectedMerits, axis=0)
EQUMeritsStd = np.std(EQUcollectedMerits, axis=0)

plt.figure()
plt.plot(ALLaveData[0]['update'], ALLMeritsMean,label = 'ALL')
plt.plot(EQUaveData[0]['update'], EQUMeritsMean,label = 'EQU')
#plt.ylim(-10,10000)
plt.legend()












#BuildPlot(DataMap = mateDisplayData[0], NamesList = ['DispAFemale', 'DispAMale'],XCoordinateName = 'update',AddLegend='bottom right')


#plt.savefig('testGraph.png', dpi=100)
plt.show()


######## SAVE TO A PDF FILE

#pp = PdfPages('foo.pdf')
#pp.savefig(fig1)
#pp.savefig(fig2)
#pp.savefig(DisplaysFig)
#pp.close()

  

