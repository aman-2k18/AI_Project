import random

maxN = 20
maxTC = 100

def main():
    f = open("nQueensTestFile.txt", "w")
    board = ""

    testCases = (maxN - 3)*maxTC
    print("Test Cases Generated!")
    board += str(testCases) + '\n'

    for n in range(4, maxN + 1):
        for tc in range(maxTC):
            board += str(n) + '\n'

            for col in range(0, n-1):
                board += str(random.randint(0, n-1)) + ' '
            
            board += str(random.randint(0, n-1)) + '\n'
    
    f.write(board)
    f.close()
    
if __name__ == '__main__':
    main()