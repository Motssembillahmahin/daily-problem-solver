# Problem: How do I store the destination filepath i copied using shutil into a variable

**Date:** 2026-10-23

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

The problem is that I would like to copy the file uploaded to a new folder called 'video store', then the name of the file that has just been copied to 'video store' is stored in a variable to be used to change the file name to the random Id number assigned to it. def loadVideo(): global filePath filePath = filedialog.askopenfilename() #original filepath randomId = random.randint(1,1000000) #upload video file shutil.copy(filePath, "video store") #file is copied to new path newPath = "/video stor

## Original URL

https://stackoverflow.com/questions/76110154/how-do-i-store-the-destination-filepath-i-copied-using-shutil-into-a-variable
