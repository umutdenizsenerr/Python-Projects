Firstly, we defined listCreator function to create the appropriate list for the best, worst, and average cases according to input size and operation number.

Then, we defined a function called func. It first creates list with listCreator function. After that, we converted the pseudo code which is provided in description of project to python. Since python's for loop doesn't have a property like "for(int k = 0; k>=1 ; k/=2)" we have to use while loop in that part of the pseudo code. 

Also we use python's numpy library in order to arrange ratio of the 0's and 1's randomly in the average case. We considered the probability without replacement case and we've fixed the ratio 1 to 3 in array. But if the given probability case is the one with replacement, we can simply use the commented line in average case in listCreator method.

We started to measure time after listCreator since the creation time of list is not related with execution time of algorithm. And we stoped the clock just before return comment in pseudo code. Time is measured in seconds.