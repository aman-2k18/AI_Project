import random
import time

FAILED = False
RESTART = False
maxTC = 100
maxRestart = 10
RES = 0

# heuristic cost
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

def generateRandomBoard(board):
    for col in range(len(board)):
        board[col] = random.randint(0, len(board) - 1)
    
    return board

# it randomly select a point until it is better than the original one change "better than" to "not worse than"
# can significantly increase the success rate
def step_FirstChoiceHillClimbing(board):
    collisionNum = collisionCount(board)
    maxRound = 200 # the expected number to find a better choice
    maxRestart = 15
    count = 0

    while True:
        count += 1

        if(count > maxRound):
            count = 0
            global RES
            RES += 1

            if RES > maxRestart:
                global FAILED
                FAILED = True
                return board
            
            global RESTART
            RESTART = True
            
            board = generateRandomBoard(board)
            collisionNum = collisionCount(board)
            return board

        rRow = random.randint(0, len(board) - 1)
        rCol = random.randint(0, len(board) - 1)

        while(board[rCol] == rRow):
            rRow = random.randint(0, len(board) - 1)

        originRow = board[rCol]
        board[rCol] = rRow

        if collisionCount(board) <= collisionNum: # not worse than
            return board

        board[rCol] = originRow
        

def solution_FirstChoiceHillClimbing(board):

    maxRound = 200 # the expected number to find a solution
    count = 0

    while True:
        collisionNum = collisionCount(board)

        if collisionNum == 0:
            return board

        board = step_FirstChoiceHillClimbing(board)

        global RESTART
        if RESTART:
            count = 0
            RESTART = False

        global FAILED
        if FAILED:
            return board
        count += 1

        if(count >= maxRound):
            FAILED = True
            return board
    
def main():
    title = "randomRestart"
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
            global FAILED, RES
            FAILED = False
            RES = 0
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