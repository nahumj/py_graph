
import matplotlib.pyplot as plt
import numpy as np
import math

line = [0]

markers = ('+','.',',','1','2','3','4','x','_','|','o','*','p','s','d','D','h','H','8','^','v','<','>')
colors = ('r','b','g','c','m','y','k')
linestyles = ['-', '--', ':', '-.']
lineWidths = [1,4,7,8]

width = 1


# the following will make some legends without plots showing marker styles and line styles
plt.figure(figsize=(10,8))
plt.subplot(1,7,1)                                         
for mark in markers: # plot some markers
  plt.plot(line, color = 'r', marker = mark, label = 'marker = \'' + mark + '\'', linewidth = width, markersize = 10, linestyle='None')
plt.axis('off')
plt.legend(loc = 'center')

plt.subplot(1,10,5)

                                  
for linedef in linestyles: # show some line styles in various line widths
  for width in lineWidths:
    plt.plot(line, color = 'k', linestyle = linedef, label = 'linestyle = \'' + linedef + '\', linewidth = \''+str(width)+'\'', linewidth = width)
  plt.plot(line,linestyle = 'None',label = ' ') # add a space in the legend between each line style

plt.plot(line,linestyle = 'None',label = 'linestyle = \'None\'') # show linestyle = 'None'
plt.axis('off')
plt.legend(loc = 'center')

width = 5
plt.subplot(1,4,4)                                         
for clr in colors: # show some colors
  plt.plot(line, color = clr, label = 'color = \'' + clr + '\'', linewidth = width)

# show a couple of custom colors
plt.plot(line, color = (1,0,.5), label = 'color = (1,0,.5)', linewidth = width)
plt.plot(line, color = (.5,.5,.25), label = 'color = (.5,.5,.25)', linewidth = width)

plt.plot(line,linestyle = 'None',label = '  ') # show the effect of alpha
plt.plot(line, color = (0,0,0), label = 'alpha = .25', linewidth = width,alpha = .25)
plt.plot(line, color = (0,0,0), label = 'alpha = .5', linewidth = width,alpha = .5)
plt.plot(line, color = (0,0,0), label = 'alpha = .75', linewidth = width,alpha = .75)

plt.plot(line,linestyle = 'None',label = '  ') # show diffrent marker sizes
plt.plot(line, color = 'r', marker = '*', label = 'markersize = 5',markersize = 5,linestyle=' ')
plt.plot(line, color = 'r', marker = '*', label = 'markersize = 10',markersize = 10,linestyle=' ')
plt.plot(line, color = 'r', marker = '*', label = 'markersize = 15',markersize = 15,linestyle=' ')

plt.plot(line,linestyle = 'None',label = '  ') # show diffrent fillstyles
plt.plot(line, color = 'r', marker = '*', label = 'fillstyle = \'none\'',markersize = 15,linestyle=' ', fillstyle='none')
plt.plot(line, color = 'r', marker = '*', label = 'fillstyle = \'top\'',markersize = 15,linestyle=' ', fillstyle='top')
plt.plot(line, color = 'r', marker = '*', label = 'fillstyle = \'bottom\'',markersize = 15,linestyle=' ', fillstyle='bottom')
plt.plot(line, color = 'r', marker = '*', label = 'fillstyle = \'left\'',markersize = 15,linestyle=' ', fillstyle='left')
plt.plot(line, color = 'r', marker = '*', label = 'fillstyle = \'right\'',markersize = 15,linestyle=' ', fillstyle='right')


plt.axis('off')
plt.legend(loc = 'center')


####### DISPLAY ALL THE FIGURES YOU HAVE MADE

#plt.show()
plt.savefig('plotStyles.png', dpi=100)

  

