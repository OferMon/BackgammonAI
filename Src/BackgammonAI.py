# v2.0.5
import os
import math
from copy import deepcopy
import random


def getInt():
    while True:
        try:
            num = int(input())
            return num
        except:
            print("Invalid input, please try again")


class Board:
    BlackInHome = False
    WhiteInHome = False
    def __init__(self):
        columns = []
        for i in range(26):
            columns.append([])
        for i in range(2):
            columns[24].append("B")
            columns[1].append("W")
        for i in range(3):
            columns[17].append("W")
            columns[8].append("B")
        for i in range(5):
            columns[13].append("B")
            columns[12].append("W")
            columns[19].append("W")
            columns[6].append("B")

        self.columns = columns

    def update_in_home(self, color):
        if color == "W":
            for i in range(19):
                if color in self.columns[i]:
                    return
            self.WhiteInHome = True
        elif color == "B":
            for i in range(7, 26):
                if color in self.columns[i]:
                    return
            self.BlackInHome = True


    def print(self):
        column_size = 5
        str = " +13-14-15-16-17-18------19-20-21-22-23-24-+ \n"
        for j in range(column_size):
            str += " |"
            for i in range(13, 19):
                if len(self.columns[i]) > j:
                    str += " " + self.columns[i][j] + " "
                else:
                    str += "   "
            if len(self.columns[25]) > j:
                str += "| " + self.columns[25][j] + " |"
            else:
                str += "|   |"
            for i in range(19, 25):
                if len(self.columns[i]) > j:
                    str += " " + self.columns[i][j] + " "
                else:
                    str += "   "
            str += "| \n"
        str += "v|                  |BAR|                  | \n"
        for j in range(column_size-1, -1, -1):
            str += " |"
            for i in range(12, 6, -1):
                if len(self.columns[i]) > j:
                    str += " " + self.columns[i][j] + " "
                else:
                    str += "   "
            if len(self.columns[0]) > j:
                str += "| " + self.columns[0][j] + " |"
            else:
                str += "|   |"
            for i in range(6, 0, -1):
                if len(self.columns[i]) > j:
                    str += " " + self.columns[i][j] + " "
                else:
                    str += "   "
            str += "| \n"
        str += " +12-11-10--9--8--7-------6--5--4--3--2--1-+"
        print(str + "\n")


    def can_move(self, color, valid_steps):
        if color == "B":
            if len(self.columns[25]) > 0:
                for i in range(19, 25):
                    if not (len(self.columns[i]) > 1 and self.columns[i][0] != "B") and (25-i) in valid_steps:
                        return True
                return False
            elif self.BlackInHome:
                found_extreme = False
                for i in range(6, 0, -1):
                    if "B" in self.columns[i]:
                        for step in valid_steps:
                            if not found_extreme and i-step <= 0:
                                return True
                            if i-step > 0 and not (len(self.columns[i-step]) > 1 and self.columns[i-step][0] != "B"):
                                return True
                            if found_extreme and i-step == 0:
                                return True
                        found_extreme = True
                return False
            else:
                for i in range(1, len(self.columns)):
                    if "B" in self.columns[i]:
                        for step in valid_steps:
                            if i-step > 0 and not (len(self.columns[i-step]) > 1 and self.columns[i-step][0] != "B"):
                                return True
                return False
        elif color == "W":
            if len(self.columns[0]) > 0:
                for i in range(1, 7):
                    if not (len(self.columns[i]) > 1 and self.columns[i][0] != "W") and i in valid_steps:
                        return True
                return False
            elif self.WhiteInHome:
                found_extreme = False
                for i in range(19, 25):
                    if "W" in self.columns[i]:
                        for step in valid_steps:
                            if not found_extreme and i + step >= 25:
                                return True
                            if i + step < 25 and not (len(self.columns[i + step]) > 1 and self.columns[i + step][0] != "W"):
                                return True
                            if found_extreme and i+step == 25:
                                return True
                        found_extreme = True
                return False
            else:
                for i in range(1, len(self.columns)):
                    if "W" in self.columns[i]:
                        for step in valid_steps:
                            if i + step < 25 and not (len(self.columns[i + step]) > 1 and self.columns[i + step][0] != "W"):
                                return True
                return False
        else:
            print("ERROR")
            exit(1)


    def move(self, color, index, steps, feedback):
        if index not in range(26) or len(self.columns[index]) == 0 or self.columns[index][0] != color:
            if feedback: print("There are no suitable soldiers in the selected column")
            return False
        if self.columns[index][0] == "W":
            if len(self.columns[0]) > 0 and index != 0:
                if feedback: print("Soldiers must be moved from the BAR")
                return False
            elif index+steps > 24:
                if self.WhiteInHome == False:
                    if feedback: print("Soldiers cannot be removed from the board")
                    return False
                else:
                    if index + steps != 25 and index != 19:
                        for i in range(19, index):
                            if "W" in self.columns[i]:
                                if feedback: print("Soldier cannot be removed from the board")
                                return False
                    self.columns[index].pop()

            elif len(self.columns[index+steps]) > 0 and self.columns[index+steps][0] == "B":
                if len(self.columns[index+steps]) == 1:
                    self.columns[25].append(self.columns[index+steps].pop())
                    self.columns[index + steps].append(self.columns[index].pop())
                    self.BlackInHome = False
                else:
                    if feedback: print("The position is occupied")
                    return False
            else:
                self.columns[index+steps].append(self.columns[index].pop())
            if not self.WhiteInHome:
                self.update_in_home(color)
            return True
        elif self.columns[index][0] == "B":
            if len(self.columns[25]) > 0 and index != 25:
                if feedback: print("Soldiers must be moved from the BAR")
                return False
            elif index - steps < 1:
                if self.BlackInHome == False:
                    if feedback: print("Soldiers cannot be removed from the board")
                    return False
                else:
                    if index - steps != 0 and index != 6:
                        for i in range(6, index, -1):
                            if "B" in self.columns[i]:
                                if feedback: print("Soldier cannot be removed from the board")
                                return False
                    self.columns[index].pop()

            elif len(self.columns[index - steps]) > 0 and self.columns[index - steps][0] == "W":
                if len(self.columns[index - steps]) == 1:
                    self.columns[0].append(self.columns[index - steps].pop())
                    self.columns[index - steps].append(self.columns[index].pop())
                    self.WhiteInHome = False
                else:
                    if feedback: print("The position is occupied")
                    return False
            else:
                self.columns[index - steps].append(self.columns[index].pop())
            if not self.BlackInHome:
                self.update_in_home(color)
            return True
        else:
            print("ERROR")
            exit(1)


    def user_move(self, color, cube1, cube2, mode):
        if mode == 1 or mode == 2:
            if mode == 1:
                self.print()
            if color == "B":
                print("Black Turn")
            elif color == "W":
                print("White Turn")
            print("Cubs: " + str(cube1) + "," + str(cube2))
        valid_steps = []
        if cube1 == cube2:
            valid_steps = [cube1, cube1, cube1, cube1]
        else:
            valid_steps = [cube1, cube2]

        while len(valid_steps) != 0:
            if not self.can_move(color, valid_steps):
                print("There are no possible steps")
                os.system('set /p DUMMY=Hit ENTER to Continue...')
                if mode == 2:
                    os.system('cls')
                return
            print("Steps to play: " + str(valid_steps))
            if color == "B" and len(self.columns[25]) > 0:
                print("BAR selected")
                column = 25
            elif color == "W" and len(self.columns[0]) > 0:
                print("BAR selected")
                column = 0
            else:
                print("select column: ")
                column = getInt()
            print("select steps: ")
            steps = getInt()
            if steps not in valid_steps:
                print("Invalid step")
            for s in valid_steps:
                if steps == s:
                    if self.move(color, column, steps, True):
                        os.system('cls')
                        self.print()
                        if color == "B":
                            print("Black Turn")
                        if color == "W":
                            print("White Turn")
                        print("Cubs: " + str(cube1)+","+str(cube2))
                        valid_steps.remove(s)
                        self.check_game_end(color)
                    break
        os.system('cls')


    def computer_move(self, color, cube1, cube2, mode, dif):
        steps = []
        temp = []
        valid_steps = []
        if cube1 == cube2:
            valid_steps = [cube1, cube1, cube1, cube1]
        else:
            valid_steps = [cube1, cube2]
        temp.append((self, valid_steps, ""))
        while len(temp) != 0:
            cur_temp = temp.pop(0)
            cur_state = cur_temp[0]
            cur_valid_steps = cur_temp[1]
            cur_trace = cur_temp[2]
            if cur_state.can_move(color, cur_valid_steps):
                if cur_valid_steps.count(cur_valid_steps[0]) == len(cur_valid_steps):
                    for i in range(26):
                        new_state = deepcopy(cur_state)
                        if new_state.move(color, i, cur_valid_steps[0], False):
                            if len(cur_valid_steps) == 1:
                                steps.append((new_state, new_state.calc_score(color), (cur_trace + "column: " + str(i) + ", steps: " + str(cur_valid_steps[0]))))
                            else:
                                c_valid_steps = cur_valid_steps.copy()
                                c_valid_steps.remove(cur_valid_steps[0])
                                temp.append((new_state, c_valid_steps, cur_trace + "column: " + str(i) + ", steps: " + str(cur_valid_steps[0]) + "\n"))
                else:
                    for step in cur_valid_steps:
                        for i in range(26):
                            new_state = deepcopy(cur_state)
                            if new_state.move(color, i, step, False):
                                if len(cur_valid_steps) == 1:
                                    steps.append((new_state, new_state.calc_score(color), (cur_trace + "column: " + str(i) + ", steps: " + str(step))))
                                else:
                                    c_valid_steps = cur_valid_steps.copy()
                                    c_valid_steps.remove(step)
                                    temp.append((new_state, c_valid_steps,  cur_trace + "column: " + str(i) + ", steps: " + str(step) + "\n"))
            else:
                new_state = deepcopy(cur_state)
                steps.append((new_state, new_state.calc_score(color), (cur_trace + "There are no possible steps")))
        steps.sort(key=score_sort)
        if len(steps) == 0:
            print("There are no possible steps")
            if mode == 2:
                os.system('set /p DUMMY=Hit ENTER to Continue...')
                os.system('cls')

            self.check_game_end(color)
            return self
        else:
            # rand = random.randint(0, dif)
            # state = steps.pop(min(rand * 2, len(steps)-1))
            state = steps.pop(min(dif * 2, len(steps)-1))

            if mode == 2:
                state[0].print()
                if color == "W":
                    print("White Turn")
                elif color == "B":
                    print("Black Turn")
                print("Cubs: " + str(cube1) + "," + str(cube2))
                print(state[2] + "\n")
            elif mode == 3:
                if color == "W":
                    print("White Turn")
                elif color == "B":
                    print("Black Turn")
                print("Cubs: " + str(cube1) + "," + str(cube2))
                print(state[2] + "\n")
                state[0].print()
            state[0].check_game_end(color)
            return state[0]


    def check_game_end(self, color):
        for col in self.columns:
            if color in col:
                return
        if color == "W":
            print("White Win!")
        elif color == "B":
            print("Black Win!")
        os.system('set /p DUMMY=Hit ENTER to Exit...')
        exit(0)


    def calc_score(self, color):
        ver = 2
        if ver == 1:
            return self.calc_score_v1(color)
        elif ver == 2:
            return self.calc_score_v2(color)
        if color == "B":
            return self.calc_score_v1(color)
        elif color == "W":
            return self.calc_score_v2(color)


    def calc_score_v2(self, color):
        score = 0
        # How many steps did I have left to empty the board? (+)
        scoreA = 0
        # How many steps are left for the opponent to empty the board? (-)
        scoreB = 0
        # The sum of the distances of the closed houses from the opponent's bar (-)
        scoreC = 0
        # The sum of the distances of the open houses from the opponent's bar
        scoreD = 0
        # I block (-)
        scoreE = 0
        # block me (+)
        scoreF = 0

        if color == "W":
            for i in range(26):

                if len(self.columns[i]) != 0 and self.columns[i][0] == "W":
                    scoreA = scoreA + (25 - i) * len(self.columns[i])

                elif len(self.columns[i]) != 0 and self.columns[i][0] == "B":
                    scoreB = scoreB + i * len(self.columns[i])

                if len(self.columns[i]) >= 2 and self.columns[i][0] == "W":
                    scoreC = scoreC + i

                elif len(self.columns[i]) == 1 and self.columns[i][0] == "W":
                    scoreD = scoreD + i

            if len(self.columns[25]) != 0:
                block_steps = []
                for i in range(19, 25):
                    if len(self.columns[i]) >= 2 and self.columns[i][0] == "W":
                        block_steps.append(25-i)
                if len(block_steps) >= 2:
                    reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
                else:
                    reasonability = 0
                scoreE = scoreE + reasonability * sum(block_steps)
            block_steps = []
            for i in range (1,7):
                if not self.can_move("B", [i]):
                    block_steps.append(i)
            if len(block_steps) >= 2:
                reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
            else:
                reasonability = 0
            scoreE = scoreE + reasonability * sum(block_steps)

            if len(self.columns[0]) != 0:
                block_steps = []
                for i in range(1, 7):
                    if len(self.columns[i]) >= 2 and self.columns[i][0] == "B":
                        block_steps.append(i)
                if len(block_steps) >= 2:
                    reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
                else:
                    reasonability = 0
                scoreF = scoreF + reasonability * sum(block_steps)
            block_steps = []
            for i in range(1, 7):
                if not self.can_move("W", [i]):
                    block_steps.append(i)
            if len(block_steps) >= 2:
                reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
            else:
                reasonability = 0
            scoreF = scoreF + reasonability * sum(block_steps)
            score = scoreA - scoreB - scoreC + scoreD - scoreE + scoreF
            return score

        elif color == "B":
            for i in range(26):

                if len(self.columns[i]) != 0 and self.columns[i][0] == "B":
                    scoreA = scoreA + (25 - i) * len(self.columns[i])

                elif len(self.columns[i]) != 0 and self.columns[i][0] == "W":
                    scoreB = scoreB + i * len(self.columns[i])

                if len(self.columns[i]) >= 2 and self.columns[i][0] == "B":
                    scoreC = scoreC + (25-i)

                elif len(self.columns[i]) == 1 and self.columns[i][0] == "B":
                    scoreD = scoreD + (25-i)

            if len(self.columns[0]) != 0:
                block_steps = []
                for i in range(1, 7):
                    if len(self.columns[i]) >= 2 and self.columns[i][0] == "B":
                        block_steps.append(i)
                if len(block_steps) >= 2:
                    reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
                else:
                    reasonability = 0
                scoreE = scoreE + reasonability * sum(block_steps)
            block_steps = []
            for i in range(1, 7):
                if not self.can_move("W", [i]):
                    block_steps.append(i)
            if len(block_steps) >= 2:
                reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
            else:
                reasonability = 0
            scoreE = scoreE + reasonability * sum(block_steps)

            if len(self.columns[25]) != 0:
                block_steps = []
                for i in range(19, 25):
                    if len(self.columns[i]) >= 2 and self.columns[i][0] == "W":
                        block_steps.append(25 - i)
                if len(block_steps) >= 2:
                    reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
                else:
                    reasonability = 0
                scoreF = scoreF + reasonability * sum(block_steps)
            block_steps = []
            for i in range(1, 7):
                if not self.can_move("B", [i]):
                    block_steps.append(i)
            if len(block_steps) >= 2:
                reasonability = math.comb(len(block_steps), 2) / float(math.comb(6, 2))
            else:
                reasonability = 0
            scoreF = scoreF + reasonability * sum(block_steps)

            score = scoreA - scoreB - scoreC + scoreD - scoreE + scoreF
            return score

        else:
            print("ERROR")
            exit(1)


    def calc_score_v1(self, color):
        score = 0
        scoreA = 0
        scoreB = 0
        scoreC = 0
        scoreD = 0
        scoreE = 0

        if color == "W":
            for i in range(26):

                if len(self.columns[i]) != 0 and self.columns[i][0] == "W":
                    # How many steps did I have left to empty the board?
                    scoreA = scoreA + (25 - i) * len(self.columns[i])

                elif len(self.columns[i]) != 0 and self.columns[i][0] == "B":
                    # How many steps are left for the opponent to empty the board?
                    scoreB = scoreB - i * len(self.columns[i])

                if len(self.columns[i]) >= 2 and self.columns[i][0] == "W":
                    for j in range(i + 1, 26):
                        if len(self.columns[j]) != 0 and self.columns[j][0] == "B":
                            # How many moves of the opponent did I block? * Loss of move
                            scoreD = scoreD - ((cache[j - i]) / total) * (j - i)

                elif len(self.columns[i]) == 1 and self.columns[i][0] == "W":
                    occupied = []
                    for j in range(i + 1, 26):
                        if len(self.columns[j]) >= 2 and self.columns[j][0] == "W":
                            occupied.append(j - i)
                        elif len(self.columns[j]) != 0 and self.columns[j][0] == "B":
                            counter = 0
                            num = j - i
                            for k in range(1, 7):
                                for o in occupied:
                                    if (num % o == 0) and (o % k == 0) and (float(num) / k > 2) and (
                                            float(num) / k <= 4):
                                        counter = counter + 1
                            # How much can the opponent eat me? * How much will I go back?
                            scoreC = scoreC + ((cache[j - i - 1] - len(occupied) - counter) / total) * (25 - i)

                if len(self.columns[25]) != 0:
                    for j in range(19, 25):
                        if len(self.columns[j]) >= 2 and self.columns[j][0] == "W":
                            # How much did I block him from leaving the bar? * The quantity in the bar
                            scoreE = scoreE - (((25 - j) / 3) * len(self.columns[25]))

            score = scoreA + scoreB + scoreC + scoreD + scoreE
            return score

        elif color == "B":
            for i in range(26):
                if len(self.columns[i]) != 0 and self.columns[i][0] == "B":
                    # How many steps did I have left to empty the board?
                    scoreA = scoreA + i * len(self.columns[i])

                elif len(self.columns[i]) != 0 and self.columns[i][0] == "W":
                    # How many steps are left for the opponent to empty the board?
                    scoreB = scoreB - (25 - i) * len(self.columns[i])

                if len(self.columns[i]) >= 2 and self.columns[i][0] == "B":
                    for j in range(i - 1, -1, -1):
                        if len(self.columns[j]) != 0 and self.columns[j][0] == "W":
                            # How many moves of the opponent did I block? * Loss of move
                            scoreD = scoreD - ((cache[i - j]) / total) * (i - j)

                elif len(self.columns[i]) == 1 and self.columns[i][0] == "B":
                    occupied = []
                    for j in range(i - 1, -1, -1):
                        if len(self.columns[j]) >= 2 and self.columns[j][0] == "B":
                            occupied.append(i - j)
                        elif len(self.columns[j]) != 0 and self.columns[j][0] == "W":
                            counter = 0
                            num = i - j
                            for k in range(1, 7):
                                for o in occupied:
                                    if (num % o == 0) and (o % k == 0) and (num / k > 2) and (num / k <= 4):
                                        counter = counter + 1
                            # How much can the opponent eat me? * How much will I go back?
                            scoreC = scoreC + ((cache[i - j - 1] - len(occupied) - counter) / total) * i

                if len(self.columns[0]) != 0:
                    for j in range(1, 7):
                        if len(self.columns[j]) >= 2 and self.columns[j][0] == "B":
                            # How much did I block him from leaving the bar? * The quantity in the bar
                            scoreE = scoreE - ((j / 3) * len(self.columns[0]))
            score = scoreA + scoreB + scoreC + scoreD + scoreE
            return score
        else:
            print("ERROR")
            exit(1)


def drop_cubs():
    cube1 = random.randint(1, 6)
    cube2 = random.randint(1, 6)
    return cube1, cube2


def score_sort(e):
    return e[1]


def statistics_init():
    combinations = []
    for c1 in range(1, 7):
        for c2 in range(1, 7):
            if c1 == c2:
                combinations.append([[c1], [c1], [c1], [c1]])
                combinations.append([[c1, c1], [c1], [c1]])
                combinations.append([[c1, c1], [c1, c1]])
                combinations.append([[c1, c1, c1], [c1]])
                combinations.append([[c1, c1, c1, c1]])
            else:
                combinations.append([[c1], [c2]])
                combinations.append([[c1, c2]])

    cache = [0] * 25
    for i in range(1, 25):
        for comb in combinations:
            flag = False
            for sub in comb:
                if sum(sub) == i:
                    flag = True
            if flag:
                cache[i] += 1

    total = sum(cache)

    return combinations, cache, total


def game():

    print("Select a game mode.")
    print("1 - player vs player")
    print("2 - player vs computer")
    print("3 - computer vs computer")
    print("your choice: ")
    mode = getInt()
    while mode > 3 or mode < 1:
        print("Invalid input, please try again")
        mode = getInt()

    os.system('cls')

    b = Board()

    if mode == 1:
        while True:
            cube1, cube2 = drop_cubs()
            b.user_move("B", cube1, cube2, mode)
            cube1, cube2 = drop_cubs()
            b.user_move("W", cube1, cube2, mode)
    elif mode == 2:
        while True:
            print("Select difficulty:")
            print("1 - low")
            print("2 - low-medium")
            print("3 - medium")
            print("4 - medium-hard")
            print("5 - hard")
            print("your choice: ")

            dif = getInt()
            if dif >= 1 and dif <= 5:
                dif = 5 - dif
                break
            os.system('cls')
            print("Invalid input")

        os.system('cls')
        b.print()
        while True:
            cube1, cube2 = drop_cubs()
            b.user_move("B", cube1, cube2, mode)
            cube1, cube2 = drop_cubs()
            b = b.computer_move("W", cube1, cube2, mode, dif)
    elif mode == 3:
        b.print()
        while True:
            cube1, cube2 = drop_cubs()
            b = b.computer_move("B", cube1, cube2, mode, 0)
            cube1, cube2 = drop_cubs()
            b = b.computer_move("W", cube1, cube2, mode, 0)


combinations, cache, total = statistics_init()
game()


