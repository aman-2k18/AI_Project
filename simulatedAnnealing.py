import random   #built-in module that we can use to make random numbers
import time     #this module provides various time-related functions
import math     #built-in module that we can use for mathematical tasks

FAILED = False
maxTC = 100

def collisionCount(board):
    HCost = 0

    row, diag1, diag2 = {}, {}, {}

    for Q1col in range(len(board)):
        Q1row = board[Q1col]

        if Q1row not in row:
            row[Q1row] = 0

        if Q1row - Q1col not in diag1:
            diag1[Q1row - Q1col] = 0

        if Q1row + Q1col not in diag2:
            diag2[Q1row + Q1col] = 0

        row[Q1row] += 1
        diag1[Q1row - Q1col] += 1
        diag2[Q1row + Q1col] += 1

    for queens in row.values():
        HCost += (queens*(queens - 1))//2

    for queens in diag1.values():
        HCost += (queens*(queens - 1))//2

    for queens in diag2.values():
        HCost += (queens*(queens - 1))//2

    return HCost

# accept the random choice with certain probability
def step_SimulatedAnnealing(board):
    temperature = len(board)**2
    annealingRate = 0.95

    while True:
        rRow = random.randint(0, len(board)-1)
        rCol = random.randint(0, len(board)-1)

        originCollisionNum = collisionCount(board)
        originRow = board[rCol]
        board[rCol] = rRow

        newCollisionNum = collisionCount(board)
        temperature = max(temperature * annealingRate, 0.02)

        if newCollisionNum < originCollisionNum:
            return board
        else:
            deltaE = newCollisionNum - originCollisionNum
            acceptProbability = min(math.exp(deltaE / temperature), 1)

            if random.random() <= acceptProbability:
                return board
            else:
                board[rCol] = originRow

def solution_SimulatedAnnealing(board):
    # the success rate will increase by increasing the maxRound
    maxRound = 100000
    count = 0

    while True:
        collisionNum = collisionCount(board)

        if collisionNum == 0:
            return board

        board = step_SimulatedAnnealing(board)
        count += 1

        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board
    
def main():
    title = "simulatedAnnealing"
    sTime = time.perf_counter()
    successCase = 0
    totalCase = 0
    result = title + " Result:\n\n"
    resultData = "N\t avgTime\t successRate\n"

    with open("nQueensTestFile.txt", "r") as ins:
        testCases = int(ins.readline())

        nStartTime = time.perf_counter()
        nSuccessCase = 0
        nTotalCase = 0

        while(testCases > 0):
            testCases -= 1

            print("Case: ", totalCase)
            global FAILED
            FAILED = False
            totalCase += 1
            nTotalCase += 1

            n = int(ins.readline())
            board = list(map(int, ins.readline().split()))

            if nTotalCase == 1:
                result += "\nFor N = " + str(n) + ": " + '\n\n'

            board = solution_SimulatedAnnealing(board)

            result += "Case #" + str(nTotalCase) + ":" + '\t\t'

            if FAILED:
                result += "Failed!"
            else:
                successCase += 1
                nSuccessCase += 1

                for col in range(len(board)):
                    result += str(board[col]) + " "

            result += "\n"

            if nTotalCase == maxTC:
                nEndTime = time.perf_counter()

                successRate = nSuccessCase / float(nTotalCase)
                avgTimeTaken = (nEndTime - nStartTime)/nTotalCase

                result += "\nAverage time taken: " + str(round(avgTimeTaken, 6)) + " secs" + '\n'
                result += "Total test cases: " + str(nTotalCase) + ", Successful test cases: " + str(nSuccessCase) + '\n'
                result += "Success Rate: " + str(successRate) + "\n\n"

                resultData += str(n) + '\t ' + str(round(avgTimeTaken, 6)) + '\t ' + str(successRate) + '\n'

                nSuccessCase = 0
                nTotalCase = 0


    eTime = time.perf_counter()
    result += "\nFor all N: " + '\n'
    result += "\nTotal time taken: " + str(eTime - sTime) + " secs" + '\n'
    result += "Total test cases: " + str(totalCase) + ", Successful test cases: " + str(successCase) + '\n'
    result += "Success Rate: " + str(successCase / float(totalCase)) + '\n'
    print(result)

    f = open(title + '.txt', 'w')
    f.write(result)
    f.close()

    f = open(title + '_resultData.txt', 'w')
    f.write(resultData)
    f.close()
        
if __name__ == '__main__':
    main()