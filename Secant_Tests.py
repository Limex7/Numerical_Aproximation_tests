import math

class parentTest:

    createdFile = [0, 0]

    def __init__(self):
        self = self

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
                    match subcase:
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
                    return [0.01, 2.01]
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


    def batchTest(self, preMade = True, times = 1000):
        functions = [[0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4], [1, 0, 1], [1, 1, 1],
                     [1, 2, 1], [1, 3, 1], [1, 4, 1], [1, 5, 1], [2, 0, 1], [2, 1, 1],
                     [2, 2, 2]]
        if preMade:
            calling = [[1,3,0]]
            if len(calling) == 0:
                for i in range(len(functions)):
                    self.batchloop(functions, functions, times, i)
            else:
                for i in range(len(calling)):
                    self.fullLoop(functions, calling, times, i, True, "a")
        else:
            funcs = input("how many functions do you want? \n")
            if funcs.isdigit():
                funcs = int(funcs)
                calling = []
                for i in range(funcs):
                    nextFunc = []
                    nextFunc.append(int(input("function group: \n")))
                    nextFunc.append(int(input("function subcase: \n")))
                    nextFunc.append(int(input("function power: \n")))
                    calling.append(nextFunc)
                for i in range(len(calling)):
                    self.batchloop(functions, calling, times, i)
            else:
                print("enter a number")


    def batchloop(self, functions, calling, times, i, pr = True, store = ""):
        BEdata = ""
        FEdata = ""
        stepData = ""
        if store == "a":
            data = ""
            self.filestuff("allValues.csv", data, store)
        for k in range(1, 3):
            BE = FE = initBE = initFE = endFE = endBE = 1000
            avgBE = avgFE = 0
            amtBEFailed = amtFEFailed = 0
            stepCount = {}
            if k == 1 and (calling[i][0] == 1 or (calling[i][0] == 2 and calling[i][1] == 1)):
                continue
            for j in range(1, times):
                if (calling[i][0] != 2 and calling[i][1] < 3):
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
                    stepCount.update({results[1]: stepCount[results[1]] + 1})
                else:
                    stepCount.update({results[1]: 1})
                if j == 1 and store == "a":
                    stepData += "\"" + str(results[1]) + "\""
                elif store == "a":
                    stepData += ",\"" + str(results[1]) + "\""
                invTrigCheck = not (calling[i][0] == 1 and calling[i][1] > 2 and rootApx == 0)
                if j == 1 and invTrigCheck:
                    initBE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                    initFE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
                    if store == "a":
                        BEdata += "\"" + str(initBE) + "\""
                        FEdata += "\"" + str(initFE) + "\""
                elif invTrigCheck: #change conditions to be store != ""
                    BE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                    FE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
                    BEdata += ",\"" + str(BE) + "\""
                    FEdata += ",\"" + str(FE) + "\""
                if j == 1:
                    checkedVals = self.errorCheck(initBE, initFE)
                    avgBE += checkedVals[0]
                    amtBEFailed += checkedVals[1]
                    avgFE += checkedVals[2]
                    amtFEFailed += checkedVals[3]
                else: #change conditions as well
                    checkedVals = self.errorCheck(BE, FE)
                    avgBE += checkedVals[0]
                    amtBEFailed += checkedVals[1]
                    avgFE += checkedVals[2]
                    amtFEFailed += checkedVals[3]
            if not (calling[i][0] == 2 and calling[i][1] == 1 and rootApx <= 0):
                endBE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                avgBE += endBE
            else:
                amtBEFailed += 1
            avgBE /= (times - 1 - amtBEFailed)
            endFE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
            avgFE += endFE
            avgFE /= (times - 1 - amtFEFailed)
            if store == "a":
                data = "\"" + str(self.functionName(calling[i])) + "\"\n" + BEdata + "\n" + FEdata + "\n" + stepData + "\n"
                self.filestuff("allValues.csv", data, store)
            self.finishedCalc(initBE, initFE, avgBE, avgFE, endBE, endFE, amtBEFailed, amtFEFailed, stepCount, calling[i], pr)

    def errorCheck(self, BE, FE):
        addBE = BEFailed  = addFE = FEFailed= 0
        if BE == 1000:
            BEFailed = 1
        else:
            addBE = BE
        if FE == 1000:
            FEFailed = 1
        else:
            addFE = FE
        return[addBE, BEFailed, addFE, FEFailed]


    # make a version to test changes in base for a^x also doesn't work for trig functions
    def fullLoop(self, functions, calling, times, i, pr = True, store = ""):
        if calling[i][0] == 1:
            changeBound = True
        else:
            changeBound = False
        if store == "a":
            data = ""
            self.filestuff("allValues.csv", data, store)
        for j in range(1, times):
            BE = FE = initBE = initFE = endFE = endBE = 1000
            BEdata = FEdata = stepData = ""
            avgBE = avgFE = amtBEFailed = amtFEFailed = 0
            stepCount = {}
            for k in range(1, times):
                if changeBound and k > j:
                    break
                t = [j, k, 2]
                initGuess = self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])
                results = self.singleTest(initGuess[0], initGuess[1], times, calling[i], t)
                rootApx = results[0]
                if results[1] in stepCount.keys():
                    stepCount.update({results[1] : stepCount[results[1]] + 1})
                else:
                    stepCount.update({results[1]: 1})
                if k == 1 and store == "a":
                    stepData += "\"" + str(results[1]) + "\""
                else:
                    stepData += ",\"" + str(results[1]) + "\""
                invTrigCheck = not (calling[i][0] == 1 and calling[i][1] > 2 and rootApx == 0)
                if k == 1 and invTrigCheck:
                    initBE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                    initFE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
                    if store == "a":
                        BEdata += "\"" + str(initBE) + "\""
                        FEdata += "\"" + str(initFE) + "\""
                elif invTrigCheck: #change conditions to be store != ""
                    BE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                    FE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
                    BEdata += ",\"" + str(BE) + "\""
                    FEdata += ",\"" + str(FE) + "\""
                if k == 1:
                    checkedVals = self.errorCheck(initBE, initFE)
                    avgBE += checkedVals[0]
                    amtBEFailed += checkedVals[1]
                    avgFE += checkedVals[2]
                    amtFEFailed += checkedVals[3]
                else: #change conditions as well
                   checkedVals = self.errorCheck(BE, FE)
                   avgBE += checkedVals[0]
                   amtBEFailed += checkedVals[1]
                   avgFE += checkedVals[2]
                   amtFEFailed += checkedVals[3]
            if not (calling[i][0] == 2 and calling[i][1] == 1 and rootApx <= 0):
                endBE = self.functionOfX(rootApx, t, calling[i][0], calling[i][1], calling[i][2])
                avgBE += endBE
            else:
                amtBEFailed += 1
            avgBE /= (times - 1 - amtBEFailed)
            endFE = rootApx - (self.offsetCalc(t, calling[i][0], calling[i][1], calling[i][2])[0] + 1)
            avgFE += endFE
            avgFE /= (times - 1 - amtFEFailed)
            if store == "a":
                data = "\"" + str(self.functionName(calling[i])) + str(j) + "\"\n" + BEdata + "\n" + FEdata + "\n" + stepData + "\n"
                self.filestuff("allValues.csv", data, store)
            self.finishedCalc(initBE, initFE, BE, FE, endBE, endFE, amtBEFailed, amtFEFailed, stepCount, calling[i], pr)

    def offsetRules(self):
        logCheck = True
        invTrigCheck = True
        if func[0] == 0:
            pass

    def singleTest(self, xi0, xi1, i, func, t):
        error = 1000
        xi2 = steps = 0
        if func[0] == 2 and func[1] == 1:
            noNegative = True
        else:
            noNegative = False
        brCond = abs(error) > (.5 * 10**-10) and self.funcRules(xi0, xi1, func, t) and not steps > 1000000
        while brCond:
            if noNegative:
                if xi0 <= 0 or xi1 <= 0:
                    break
            xi2 = xi1 - self.functionOfX(xi1, t, func[0], func[1], func[2]) * (xi1 - xi0)/(self.functionOfX(xi1, t, func[0], func[1], func[2]) - self.functionOfX(xi0, t, func[0], func[1], func[2]))
            xi0 = xi1
            xi1 = xi2
            error = xi1 - xi0
            steps += 1
            brCond = abs(error) > (.5 * 10**-10) and self.funcRules(xi0, xi1, func, t) and not steps > 1000000
        return [xi2, steps]

    def funcRules(self, xi0, xi1, func, t):
        rule1 = not (self.functionOfX(xi1, t, func[0], func[1], func[2]) - self.functionOfX(xi0, t, func[0], func[1], func[2])) == 0
        rule2 = True
        if func[0] == 1:
            a = xi0 % math.pi
            b = xi1 % math.pi
            if func[1] == 3:
                rule2 = a != 0 and b != 0
            elif func[1] == 4:
                rule2 = a != 1 and b != 1
            elif func[1] == 5:
                rule2 = a != 0 and b != 1
        return rule1 and rule2



    def finishedCalc(self, iBE, iFE, aBE, aFE, eBE, eFE, tfBE, tfFE, sc, func, pr = True):
        count = sum(sc.values())
        keys = sc.keys()
        keys = list(keys)
        avg = highest = highestVal = lowestSteps = highestSteps = 0
        for i in range(len(keys)):
            if sc.get(keys[i]) > highest:
                highest = sc.get(keys[i])
                highestVal = keys[i]
            if keys[i] > highestSteps:
                highestSteps = keys[i]
            elif keys[i] < lowestSteps or lowestSteps == 0:
                lowestSteps = keys[i]
            avg += sc.get(keys[i]) * keys[i]
        avg /= count
        functionName = self.functionName(func)
        if pr:
            print(str(functionName) + ": \nBackwards error Initial: " + str(iBE) + "\nForwards error Initial: " + str(
                iFE) + "\nBackwards error end: " + str(eBE) + "\nForwards error end: " + str(
                eFE) + "\navg steps: " + str(avg) + "\nmode steps: " + str(highestVal))
            print()
        else:
            values = ("\"" + str(functionName) + "\"\n" + "\"" +
                      str(iBE) + "\",\"" + str(eBE) + "\",\"" + str(aBE) + "\",\"" + str(tfBE) + "\",\"" +
                      str(iFE) + "\",\"" + str(eFE) + "\",\"" + str(aFE) + "\",\"" + str(tfFE) + "\",\"" +
                      str(lowestSteps) + "\",\"" + str(highestSteps) + "\",\"" + str(avg) + "\",\"" + str(
                        highestVal) + "\"\n")
            self.filestuff("data.csv", values)

    def filestuff(self, fileName="data.txt", data="", store = ""):
        if self.createdFile[0] == 0 and store != "a":
            with open(fileName, "w") as f:
                f.write("")
            self.createdFile[0] = 1
        elif self.createdFile[1] == 0 and store == "a":
            with open(fileName, "w") as f:
                f.write("")
            self.createdFile[1] = 1
        with open(fileName, "a") as f:
            f.write(data)


p1 = parentTest()
p1.batchTest()
