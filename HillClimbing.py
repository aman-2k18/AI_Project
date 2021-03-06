import random #built-in module that you can use to make random numbers
import time #this module provides various time-related functions

FAILED = False
maxTC = 100

# heuristic cost
def cCount(board):
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

# it randomly select a point until it is better than the original one change "better than" to "not worse than"
# can significantly increase the success rate
def step_FirstChoiceHillClimbing(board):
    cNum = cCount(board)
    maxRound = 1000 # the expected number to find a better choice
    count = 0

    while True:
        count += 1

        if(count > maxRound):
            global FAILED
            FAILED = True
            return board

        rRow = random.randint(0, len(board) - 1)
        rCol = random.randint(0, len(board) - 1)

        while(board[rCol] == rRow):
            rRow = random.randint(0, len(board) - 1)

        originRow = board[rCol]
        board[rCol] = rRow

        if cCount(board) <= cNum: # not worse than
            return board

        board[rCol] = originRow
        

def solution_FirstChoiceHillClimbing(board):

    maxRound = 200 # the expected number to find a solution
    count = 0

    while True:
        cNum = cCount(board)

        if cNum == 0:
            return board

        board = step_FirstChoiceHillClimbing(board)

        global FAILED
        if FAILED:
            return board
        count += 1

        if(count >= maxRound):
            FAILED = True
            return board
    
def main():
    title = "hillClimbing"
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

            board = solution_FirstChoiceHillClimbing(board)

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
    f.close
        
if __name__ == '__main__':
    main()