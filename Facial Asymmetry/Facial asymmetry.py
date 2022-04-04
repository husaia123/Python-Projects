"""
23380159.py
A program to anylise facial 3D measurement data to determine the correlation to certain syndromes
by: Amir Husain
start: 01/04/22
end: 02/04/22
1. A list containing the 3Dasymmetry values of each of the 9 facial landmarks.
2. A list containing the minimum(non-zero) 3Dasymmetry of the upper and lowerface.
3. A list containing the maximum(non-zero) 3Dasymmetry of the upper andlowerface.
4. A list containing the average 3Dasymmetry of the upper and lowerface.
5. A list containing the standard deviation of the 3Dasymmetry of the upper and lowerface.
main('asymmetry_sample.csv','C4996','stats')

1. A single value that is the correlation of the 3D asymmetry values of all 9 landmarks between the pair of adults
main('asymmetry_sample.csv','G8328','stats')
"""

def main(csvfile, adults, type):
    data = open(csvfile, "r")
    
    if type == "stats":#adults into list if not already a.k.a "stats" single adult
        adults = [adults]
        
    adult1, adult2 = pre_processing(data, adults, type)#if type == "stats" then adult2 = []

    if adult1[9][2:] != ['0','0','0']:#calibrates if point 10 != all 0
        adult1 = calibrate (adult1)
    if type == "corr":
        if adult2[9][2:] != ['0','0','0']:
            adult2 = calibrate (adult2)
                
    if type == "stats":
        return (stats(adult1))
    
    else:
        return (corr(adult1, adult2))
        
def pre_processing (data, adults, type):#gathers requested data
    adult1= []
    adult2= []
    for line in data:
        if line[:line.index(',')] in adults:#if text before ',' (ID) in adults (ID/s needed)
            line = line[:-1] #deletes \n at the end of the line
            line = line.split(",")#splits the rows to list with ","
            if line[0] == adults[0]:
                adult1.append(line)#adds points (line) to 2d array
            elif type == "corr":#add to adults2 if 2 adults
                adult2.append(line)
                
    adult1.sort(key=lambda point: int(point[1]))#sorts the array 
    adult2.sort(key=lambda point: int(point[1]))
    
    data.close()#file can be closed after data is gathered and calibrated
    return adult1, adult2

def calibrate (adult_array):#calibrates to point 10 0,0,0 if not already
    for point in range (9):
        for axis in range (2, 5):
            adult_array[point][axis] = float(adult_array[9][axis])-float(adult_array[point][axis])
    adult_array[9][2:] = [0,0,0]#note all changed from str to float
    return (adult_array)

def asym(adult_array):
    asym3D = []
    
    for point in range (9):#each point on face
        sum_axis_squared = 0.0
        for axis in range (2, 5):#only the axis
            sum_axis_squared += float(adult_array[point][axis])**2#adds the squared of all axis for 1 point 
        asym3D.append (sum_axis_squared**0.5)
    
    return asym3D

def stats (adult_array):
    std_sum_UP = 0
    std_sum_LOW = 0
    
    asym3D = asym(adult_array)

    mn = [round (min (asym3D[:5]),4), round (min (asym3D[5:]), 4)]#min of upper and lower 
    mx = [round (max (asym3D[:5]),4), round (max (asym3D[5:]), 4)]
        
    avg = [(sum (asym3D[:5]))/5, (sum (asym3D[5:]))/4]#doesnt round since it will be used for calculations
    
    for point in range (9):#sum of (dis - avg)^2
        if point < 5:#upper face only 
            std_sum_UP += (asym3D[point]-avg[0])**2
        else:
            std_sum_LOW += (asym3D[point]-avg[1])**2
            
    std = [round ((std_sum_UP/5)**0.5, 4), round ((std_sum_LOW/4)**0.5, 4)]
    asym3D = [round (dist, 4) for dist in asym3D]
    avg = [round (av,4) for av in avg]

    return (asym3D, mn, mx, avg, std)

def corr(adult1, adult2):
    top = 0
    sum_bot_1 = 0
    sum_bot_2 = 0
    
    asym3D1 = asym(adult1)
    asym3D2 = asym(adult2)
        
    avg1 = sum(asym3D1)/9
    avg2 = sum(asym3D2)/9
    
    for dist in range (9):
        sum1 = asym3D1[dist]-avg1
        sum2 = asym3D2[dist]-avg2#difference from value to mean

        top += (sum1)*(sum2)#sum of differnce
        
        sum_bot_1 += sum1**2#sum of difference^2
        sum_bot_2 += sum2**2
        
    bot = (sum_bot_1*sum_bot_2)**0.5
    return (round(top/bot,4))      
