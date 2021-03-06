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

RepMin = 101
RepMax = 105
maxTime = 10000                          # how many updated in this data?
outputStep = 25                          # how often was data written?

NumReps = RepMax - RepMin + 1            # how many reps are there? used mostly in range(NumReps)
RepRange = range(RepMin, (RepMax + 1))   # a range i.e. [101,102,103,104...] used when we need to know the actual number

# make some containers
aveData = []
mateDisplayData = []

# read in the data for all reps
for rep in RepRange:
  aveData.append(ReadDataFile('AvidaData/'+str(rep)+'/data/average.dat', ['update','merit'], Separator=' ', SkipRows=19))
  mateDisplayData.append(ReadDataFile('AvidaData/'+str(rep)+'/data/mating_display_data.dat', ['update','DispAUndef','DispAFemale','DispAMale'], Separator=' ', SkipRows=10))

features = {'colors':['black','white','green'],'shapes':['square','circle','triangle'],'pets':['cat','dog','bird']}

WriteDataFile('TestFile.txt', features, ['pets','colors','shapes'], Separator=':', FormatStyle='rows', PrintHeader = 'tall', Title = "some more info...")

#BuildMultiPlot(DataMap = mateDisplayData[0], NamesList = ['DispAFemale', 'DispAMale'],XCoordinateName = 'update')
#BuildMultiPlot(DataMap = mateDisplayData[0], NamesList = ['DispAFemale', 'DispAMale'], Columns = 2)
#DisplaysFig = BuildPlot(DataMap = mateDisplayData[0], NamesList = ['DispAFemale', 'DispAMale'],XCoordinateName = 'update',AddLegend='upper left')

###########################
# calculate the mean and standard devation for merit, male display and female display
###########################

# make containers
allMerits = []
allMaleDisps = []
allFemaleDisps = []

# collect the datas into one list
for index in range(NumReps):
  allMerits.append(aveData[index]['merit'])
  allMaleDisps.append(mateDisplayData[index]['DispAMale'])
  allFemaleDisps.append(mateDisplayData[index]['DispAFemale'])

# get mean and Std
MeritsMean = np.mean(allMerits, axis=0)
MeritsStd = np.std(allMerits, axis=0)
MaleDispMean = np.mean(allMaleDisps, axis=0)
MaleDispStd = np.std(allMaleDisps, axis=0)
FemaleDispMean = np.mean(allFemaleDisps, axis=0)
FemaleDispStd = np.std(allFemaleDisps, axis=0)

######## MAKE A FIGURE WITH some SUBPLOTS

# define some standards
fontSizeTitle = 16
fontSizeLegend = 10
fontSizeNormal = 10

###########################
# make a graph with raw data and a mean
###########################

# make a figure
plt.figure(figsize=(10,12))                                  
# make a subplot that will take up the upper 1/4 of the figure (all of the first row)
plt.subplot(4,1,1)

# plot all reps raw data with alpha .2
for index in range(NumReps):
  # plot merit/update, set the lable for this line to 'Merit'
  plt.plot(aveData[0]['update'],aveData[index]['merit'],label='merit('+str(RepRange[index])+')',alpha = .2)

# plot the mean
plt.plot(aveData[0]['update'],MeritsMean,label='average merit',color = 'g', linewidth = 2)

# add some formatting
plt.legend(loc='upper left', shadow=True, fontsize=fontSizeLegend) # add a legend to the upper left corner
plt.title('Merit (over Time)', fontsize=fontSizeTitle,fontweight='bold') # set the title
plt.xlabel('Time (updates)')                                # set the x axis label
plt.ylabel('Merit')                                         # set the y axis label

###########################
# make a graph with a mean and standard error
###########################

# make a subplot that will take up the second 1/4 of the figure (all of the second row)
plt.subplot(4,1,2)

# plot the mean
plt.plot(aveData[0]['update'],MeritsMean,color = 'g', linewidth = 2) # plot merit/update


# add some formatting
plt.title('Merit (over Time) with Standard Error', fontsize=fontSizeTitle,fontweight='bold') # set the title
plt.xlabel('Time (updates)')                                # set the x axis label
plt.ylabel('Merit')                                         # set the y axis label

# plot the error
plt.fill_between(aveData[0]['update'],MeritsMean-MeritsStd,MeritsMean+MeritsStd,color = 'g',alpha=.15)  # plot merit/update, set the lable for this line to 'Merit'



###########################
# make a boxplot with merit at various times
###########################

# first, lets extract some data...
meritExtractedDisp = []                                     # make a holder
timesOfInterest = [0.1,.25,.50,.75,1.0]                     # a list of times we are intersted in (ratio of total data)

# extract merits from all reaps for the times we are interested in and group them by time
for timeIndex in range(len(timesOfInterest)):
  # this finds the correct index baised on how big the data is
  time = int(timesOfInterest[timeIndex]*len(aveData[index]['merit'])-1)
  # make sub containers for each time
  meritExtractedDisp.append([])
  # add merits from all reps for this time to the sub container for this time
  for index in range(NumReps):
    meritExtractedDisp[timeIndex].append(aveData[index]['merit'][time])

# now lets plot!
# this subplot will take up the left side of the third row
plt.subplot(4,2,5)

# make a boxplot!
plt.boxplot(meritExtractedDisp)

# set the X label (positions, name)
plt.xticks(range(1,len(timesOfInterest)+1), [int(x*maxTime) for x in timesOfInterest])

# add some formatting
plt.title('Merit (over Time)', fontsize=fontSizeTitle,fontweight='bold') # set the title
plt.xlabel('Time (in Updates)')                             # set the x axis label
plt.ylabel('Merit')                                         # set the y axis label

###########################
# make a graph with male and female display
###########################

# this subplot will take up the bottom right corner
plt.subplot(2,2,4)

# plot the male and female average displays
plt.plot(aveData[0]['update'],MaleDispMean,color = 'r',label='Female Display',linewidth=3)
plt.plot(aveData[0]['update'],FemaleDispMean,color = 'b',label='Male Display',linewidth=3)

# plot deviations
plt.fill_between(aveData[0]['update'],MaleDispMean-MaleDispStd,MaleDispMean+MaleDispStd,color = 'r',alpha=.25)
plt.fill_between(aveData[0]['update'],FemaleDispMean-FemaleDispStd,FemaleDispMean+FemaleDispStd,color = 'b',alpha=.25)

# add some formatting
plt.legend(loc='upper left', shadow=True, fontsize=fontSizeLegend) # add a legend
plt.title('Display (over Time)', fontsize=fontSizeTitle,fontweight='bold') # set the title
plt.xlabel('Time (updates)')                                # set the x axis label
plt.ylabel('Average Display')                               # set the y axis label

# this subplot will take up the bottom left corner (bottom left of fourth row)
plt.subplot(4,2,7)

# plot all reps merit at alpha .2
for index in range(NumReps):
  plt.plot(aveData[0]['update'],aveData[index]['merit'],label='merit('+str(RepRange[index])+')',alpha = .2)

# there is too much data here to see error bars, lets look at only every 25th entry

# make some containers to hold sparse data
sparseMeritsMean = []
sparseMeritsStd = []
sparseUpdates = []

# add every 25th element to the spare containers
for index in np.arange(0,len(MeritsMean),25):
  sparseMeritsMean.append(MeritsMean[index])
  sparseMeritsStd.append(MeritsStd[index])
  sparseUpdates.append(aveData[0]['update'][index])

# plot mean merit with error bars
plt.plot(aveData[0]['update'],MeritsMean,label='average merit',color = 'g', linewidth = 2)
plt.errorbar(sparseUpdates,sparseMeritsMean,yerr=sparseMeritsStd, fmt='--o')

# add some formatting
plt.title('Merit with Error Bars', fontsize=fontSizeTitle,fontweight='bold') # set the title
plt.xlabel('Time (updates)')                                # set the x axis label
plt.ylabel('Average Display')                               # set the y axis label


# this tweaks the plot to make things lok beter
plt.tight_layout(pad = 1, w_pad = 2, h_pad = 0.0) # change the padding, numbers are reletive to font size




#plt.ylim(ymin = 25, ymax = 57)

####### DISPLAY ALL THE FIGURES YOU HAVE MADE

plt.savefig('testGraph.png', dpi=100)
plt.show()


######## SAVE TO A PDF FILE

#pp = PdfPages('foo.pdf')
#pp.savefig(fig1)
#pp.savefig(fig2)
#pp.savefig(DisplaysFig)
#pp.close()

  

