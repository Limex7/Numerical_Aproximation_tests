import math

# For ease of plugging in functions
def functionOfX(x, a):
    return (math.e**x - a) #placeholder for now

# tests a range of values of a in different ways
def parentTesting():
    for i in range(1,1000000):
        xi0 = math.log(i, math.e) - 1
        xi1 = math.log(i, math.e) + 1
        error = 1000
        steps = 0

        while abs(error) > 0 and not (functionOfX(xi1, i) - functionOfX(xi0, i)) == 0:
            xi2 = xi1 - functionOfX(xi1, i) * (xi1 - xi0) / (functionOfX(xi1, i) - functionOfX(xi0, i))
            xi0 = xi1
            xi1 = xi2
            error = xi1 - xi0
            steps += 1

        finishedCalc(xi2, steps, i)

# Printing function
def finishedCalc(xi2, steps, i):
    print(xi2)
    print(steps)
    print("Backwards Error " + str(functionOfX(xi2, i)))
    print()

parentTesting()
