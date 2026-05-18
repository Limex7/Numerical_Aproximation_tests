import math

class parentTest:

    def __init__(self):
        self = self

    #returns the function of x
    def functionOfX(self, x, t, func = 0, subcase = 0, pow = 1):
        match func:
            case 0:
                return(t[0]*x**pow - t[1])
            case 1:
                match subcase:
                    case 0:
                        return(t[0]*math.sin(x) - t[1])
                    case 1:
                        return(t[0]*math.cos(x) - t[1])
                    case 2:
                        return(t[0]*math.tan(x) - t[1])
                    case 3:
                        return(t[0]*math.sin(x)**(-1) - t[1])
                    case 4:
                        return(t[0]*math.cos(x)**(-1) - t[1])
                    case 5:
                        return(t[0]*math.tan(x)**(-1) - t[1])
            case 2:
                match subcase:
                    case 0:
                        return(t[0]*math.e**x - t[1])
                    case 1:
                        return(t[0]*math.log(x, t[2]) - t[1]) # do not change order of t vars
                    case 2:
                        return(t[0]*t[2]**x - t[1]) # do not change order of t vars
        return(0)


    # returns xi0 and xi1 do not put in 0 for t[0]
    def offsetCalc(self, t, func = 0, subcase = 0, pow = 1):
        ca = t[1] / t[0]
        match func:
            case 0:
                if t[1] > 0:
                    root = ca**(1/pow)
                    return [root - 1, root + 1]
                else:
                    return [-1, .99]
            case 1:
                if (abs(ca) <= 1 and subcase < 3) or (abs(ca) >= 1 and subcase >= 3):
                    match subcase: # trig shifts might need to be lowered
                        case 0:
                            root = math.asin(ca)
                        case 1:
                            root = math.acos(ca)
                        case 2:
                            root = math.atan(ca)
                        case 3:
                            root = math.asin(ca**(-1))
                        case 4:
                            root = math.acos(ca**(-1))
                        case 5:
                            root = math.atan(ca**(-1))
                    return [root - 1, root + .99]
                else:
                    return [0, 2]
            case 2:
                if t[0] > 0:
                    match subcase:
                        case 0:
                            root = math.log(ca, math.e)
                        case 1:
                            root = t[2]**(ca)
                        case 2:
                            if ca >= 0:
                                root = math.log(ca, t[2])
                    return [root - 1, root + 1]

    #returns function name for printing
    def functionName(self, func):
        match func[0]:
            case 0:
                return "x^" + str(func[2])
            case 1:
                match func[1]:
                    case 0:
                        return "sin(x)"
                    case 1:
                        return "cos(x)"
                    case 2:
                        return "tan(x)"
                    case 3:
                        return "csc(x)"
                    case 4:
                        return "sec(x)"
                    case 5:
                        return "cot(x)"
            case 2:
                match func[1]:
                    case 0:
                        return "e^x"
                    case 1:
                        return "log(x)"
                    case 2:
                        return str(func[2]) + "^x"

    #does a bunch of secant approximations 
    def batchTest(self, preMade = True, times = 1000):
        functions = [[0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4], [1, 0, 1], [1, 1, 1],
                     [1, 2, 1], [1, 3, 1], [1, 4, 1], [1, 5, 1], [2, 0, 1], [2, 1, 1],
                     [2, 2, 2]]
        if preMade:
            calling = []
            if len(calling) == 0:
                self.batchloop(functions)
            else:
                self.batchloop(functions, calling)
        else:
            funcs = input("how many functions do you want to test?\n")
            calling = []
            for i in range(funcs):
                nextFunc = []
                nextFunc.append(input("function group: \n"))
                nextFunc.append(input("function subcase: \n"))
                nextFunc.append(input("function power: \n"))
                calling.append(nextFunc)
            

    def batchloop(self, functions, calling = functions):
        for i in range(len(functions)):
            for k in range(1, 3):
                initBE = initFE = endFE = endBE = 1000
                stepCount = {}
                if k == 1 and (calling[i][0] == 1 or (calling[i][0] == 2 and calling[i][1] == 1)):
                    continue
                for j in range(1, times):
                    if (calling[i][0] != 2 or calling[i][1] < 3):
                        if k == 1:
                            t = [1, j, 2]
                        else:
                            t = [j, 1, 2]
                    else:
                        t = [j, j, 2]
                    initGuess = self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])
                    results = self.singleTest(initGuess[0], initGuess[1], times, calling[i], t)
                    rootApx = results[0]
                    if results[1] in stepCount.keys():
                        stepCount.update({results[1]:stepCount[results[1]] + 1})
                    else:
                        stepCount.update({results[1]:1})
                    if j == 1 and not(calling[i][0] == 1 and calling[i][1] > 2 and rootApx == 0):
                        initBE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                        initFE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
                if not(calling[i][0] == 2 and calling[i][1] == 1 and rootApx <= 0):
                    endBE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                else:
                    endBE = -1
                endFE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
                self.finishedCalc(initBE, initFE, endBE, endFE, stepCount, calling[i])
                    

    #finds the secant approximation and counts the step for a particular function returns steps and approximation
    def singleTest(self, xi0, xi1, i, func, t):
        error = 1000
        xi2 = steps = 0
        hold = [0, 0]
        if func[0] == 2 and func[1] == 1:
            noNegative = True
        else:
            noNegative = False
        brCond = abs(error) > (.5 * 10**-10) and not (self.functionOfX(xi1, t, func[0], func[1], func[2]) - self.functionOfX(xi0, t, func[0], func[1], func[2])) == 0 and not steps > 100000
        while brCond:
            if noNegative:
                if xi0 <= 0 or xi1 <= 0:
                    break
            xi2 = xi1 - self.functionOfX(xi1, t, func[0], func[1], func[2]) * (xi1 - xi0)/(self.functionOfX(xi1, t, func[0], func[1], func[2]) - self.functionOfX(xi0, t, func[0], func[1], func[2]))
            xi0 = xi1
            xi1 = xi2
            error = xi1 - xi0
            steps += 1
            brCond = abs(error) > (.5 * 10**-10) and not (self.functionOfX(xi1, t, func[0], func[1], func[2]) - self.functionOfX(xi0, t, func[0], func[1], func[2])) == 0 and not steps > 100000
        return [xi2, steps]



    #just a printing function
    def finishedCalc(self, iBE, iFE, eBE, eFE, sc, func):
        count = sum(sc.values())
        keys = sc.keys()
        keys = list(keys)
        avg = 0
        highest = 0
        highestVal = 0
        for i in range(len(keys)):
            if sc.get(keys[i]) > highest:
                highest = sc.get(keys[i])
                highestVal = keys[i]
            avg += sc.get(keys[i]) * keys[i]
        avg /= count
        functionName = self.functionName(func)
        print(str(functionName) + ": \nBackwards error Initial: " + str(iBE) + "\nForwards error Initial: " + str(iFE) + "\nBackwards error end: " + str(eBE) + "\nForwards error end: " + str(eFE) + "\navg steps: " + str(avg) + "\nmode steps: " + str(highestVal))
        print()


p1 = parentTest()
p1.batchTest()


