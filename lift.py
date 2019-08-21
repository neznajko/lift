#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse # ---------------------------------------------------- 0
import re # regular expresions --------------------------------------- 1
from collections import deque # -------------------------------------- 2
from os import system # ---------------------------------------------- 3
from random import randint, sample # --------------------------------- 4
from copy import deepcopy # ------------------------------------------ 5
import sys #---------------------------------------------------------- 6
from numpy.random import poisson # ----------------------------------- 7
import time # -------------------------------------------------------- 8

# ĝlobal stu£f ####################################################### 0
args = None # command line arguments                                   1
request = deque() # user requests per unit time                        2

def getdir(a, b): return (a > b) - (a < b) # :::ƀoØm:::::::::::::::::: 0

class Terran: ######################✖#❆############################### 0
    def __init__(self, orig, dest): # |                                1
        self.orig = orig #            |                                2
        self.dest = dest #            |                                3
        self.dir = getdir(dest, orig) #_______________________________ 4

    def __str__(self): #####################█######################### 0
        return f"{self.orig} ▷ {self.dest}" #__________________⌘______ 1

def gen_scv(): # :< man witℎ dro☢ped mustaches ``ƽ∈``````````````````` 0
    nscv = poisson(args.λ) # num|er of scvs enter||g ze command center 1
    start = 1 ##########ǝ#######|################||################### 2
    stop = args.nfloors #       |                ||                    3
    step = 1 #                  |                ||                    4
    if args.mode is 1: step = 2 #                ||                    5
    for j in range(nscv): #                      ||                    6
        if args.mode is 1: start = randint(1, 2) #|                    7
        ls = [0] + list(range(start, stop, step)) #                    8
        orig, dest = sample(ls, 2) ########ƃ########################## 9
        request.append(Terran(orig, dest)) # __________,'`".__________ 0

def get_infut(regex): # fill request from ∂e infut ################### 0
    it = map(int, regex.findall(input())) # iterator                   1
    for j in it: ###########################≈######################### 2
        request.append(Terran(j, next(it))) # _______________⚆-------- 3

def assign2min(req, lift): ########Ě#∗##∏############################# 0
    ls = [j.request for j in lift] # |  | make list with lift requests 1
    j = ls.index(min(ls, key = len)) #  |  find the index with min len 2
    lift[j].request.append(req) #       |             register request 3
    lift[j].queue[req.orig].append(req) # _____⎟_______ register queue 4

def assign(lift): ### a↋sign requestή ✚✪ lift ######################## 0
    if args.mode is 0: #            | ||                   normal mode 1
        while request: #            | ||                               2
            req = request.popleft() # ||                               3
            assign2min(req, lift) ##∑#||############################## 4
    else: ##########################|#||########### partition requests 5
        ls = lift[0::2], lift[1::2] # ||       even, odd indexed lifts 6
        while request: #############✠#||############################## 7
            req = request.popleft() # ||                               8
            if req.orig: n = req.orig #|                dodge the zero 9
            else: n = req.dest #       |                               0
            assign2min(req, ls[n % 2]) # _____________________________ 1

def scvstr(scvs): # concatenate scvs' request striⲊgs ################ 0
    return ', '.join([j.__str__() for j in scvs]) #_____________✘_____ 1

class Lift: ################✖#######ə#######################ʎ######### 0
    def __init__(self, id): #       |                       |          1
        self.id = id ######℥########|#######################|######### 2
        self.cycle = False # if True|jump to next clock cyclę          3
        self.action = self.wait4req # ze action function    |          4
        self.request = deque() # external requests          |          5
        self.queue = [deque() for f in range(args.nfloors)] #          6
        self.exitstk = [] # stack repræsenting lift's pressed buttons  7
        self.ntastk = [] # stack with ℙeople entering the lift         8
        self.dir = 0 #################|################ lift direction 9
        self.floor = args.nfloors - 1 # lift floor                     0
        self.task = None # cÙrrent request                             1
        self.ignore = False # ignore flag                              2

    def __str__(self): ####################ℯ#################### Śebuk 0
        a = f'({self.floor}) ❮{self.dir}❯' #                           1
        b = scvstr(self.request) ##########################±########## 2
        c = self.action.__name__ #                         |           3
        d = ', '.join(map(lambda j: str(j), self.exitstk)) #           4
        e = scvstr(self.ntastk) ###########¦########################## 5
        f = scvstr(self.queue[self.floor]) #########¿################# 6
        return f'{a} [{b}] {c} ❬❬{d}❭❭ «{e}» ❲{f}❳' #_________________ 7
  
    def wait4req(self): #####Œő#####Ŕ#################―############### 0
        if not self.request: #|empty|req stk?         |                1
            self.cycle = True # clckØext wait for req |   _  _ __A__ _ 2
            return #################|#################|############### 3
        self.task = self.request[0] # copy Ninja Kakashi               4
        self.dir = getdir(self.task.orig, self.floor) #                5
        self.ignore = (self.dir != self.task.dir) #                    6
        self.action = self.queueck # ck ze wating queue ______°_______ 7

    def ck(self, req): #########ыℜ#########⌇########################## 0
        self.ntastk.append(req) # nta      |                           1
        self.request.remove(req) # ck      |                           2
        self.queue[self.floor].remove(req) #__ʐ_______________________ 3

    def queueck(self): ################⊲#Ö############################ 0
        queue = self.queue[self.floor] # |                             1
        if queue: ####################ś##|############################ 2
            if self.task == queue[0]: #  |                             3
                self.dir = self.task.dir #                             4
                self.ignore = False ###Œ############################## 5
                self.task = None ######|####################jobs done! 6
        if self.ignore: #              |                               7
            self.action = self.justGou #                               8
            return ################################################### 9
        # bug namba 342: Here ve have to enclose ze deque in a list()  0
        # unless we want a «deque mutated during iteration» exception  1
        for req in list(queue): ####«############# same directions ck  2
            if self.dir == req.dir: ##??############################## 3
                self.ck(req) # 4k the req                              4
        if self.ntastk: ###########£################################## 5
            self.action = self.nta # vaita one cycle and zen Gou       6
            self.cycle = True #               _                        7
        else: # neva beginze(HuKora He §ano4Bau nptB BuHaru..)         8
            self.action = self.justGou #_______¥______________________ 9

    def justGou(self): ########⨱###❰################################## 0
        self.floor += self.dir #___|__________________________________ 1
        self.action = self.arvedon #                                   2
        self.cycle = True #____________________✔______________________ 3

    def nta(self): #---Ctc ⊤a3u ▖ecHù4ka n♻3gpaBs♥aM BcsKa nu4Ka------ 0
        while self.ntastk: #        |     |      |                     1
            scv = self.ntastk.pop() #     |      |                     2
            self.exitstk.append(scv.dest) #      |                     3
        self.exitstk = sorted(set(self.exitstk)) #  rm duples and sort 4
        if self.dir < 0: ##########ś################################## 5
            self.exitstk.reverse() #                                   6
        self.action = self.justGou #____________________________∞_____ 7

    def arvedon(self): ##Ɔ####################č####################### 0
        if self.exitstk: #                    |                        1
            if self.floor == self.exitstk[0]: #                        2
                self.action = self.exit #                              3
                return ############ƺ################################## 4
        self.action = self.queueck #________ɱ_________________________ 5

    def exit(self): ########Ç#################∷####################### 0
        del self.exitstk[0] # turn off ze button                       1
        if not (self.exitstk or self.task): ############## ck if empty 2
            self.action = self.wait4req # wait for requests            3
        else: # *∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*ÿ*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗*∗ 4
            self.action = self.queueck # ck waiting queue              5
        self.cycle = True # wait one cycle on ze floor ____ƽ__________ 6
########Ö#######ö#######O#######ò#######o#######6#######0#######
#       |       |       |       |       |       |       |       
CSI = '\033[' ##########|############Control#Sequence#In|roducer
#       |       |       |       |       |       |       |
def ClrStr(type, clr): #|###############|#######get#color#string
    """ ########¦#######|###############¦#######¦#######:#######
    infut: type: 0 - foreground, 1 - background
           clr:  rgb list
    oufut: formated string for colored oufut
    xmple: ';38;2;120;30;40' <- ClrStr(0, [120, 30, 40])
    notes: 'clr can be empty (for transparent background)
    """ ########|#######¦#######'#######|#######;#######|#######
    ClrStr.code = [';38;2', ';48;2'] #  ¦       |    static data
    if clr: #   ¦       |       |       '       ¦ck if not empty
        clr = (';{}' * 3).format(*clr) #.       |   do the mambo
    else: ######,#######|#######¦#######¦#######|#######|#######
        return '' #     ¦       :       |no colo'r (tran|parent)
    return ClrStr.code[type] + clr #    ¦       '       `  Yeah!
#       |       '       |       ¦       |       |       |
def SgrStr(sgr): #######|####get#Select#Graphic#Rendition#string
    """ ########|#######'#######,#######¦#######¦#######'#######
    infut: sgr: list
    oufut: formated string 4 colored oufut
    xmple: ';5' <- SgrStr([5])
    notes: none
    """ ########,#######|#######¦#######,#######'#######¦#######
    if not sgr: return '' #     |       |       ¦       ,       
    return ';' + ';'.join([str(j) for j in sgr]) #      |
#       ¦       |       |       |       |       |       |
def Display(x, y, fgr, bgr, sgr, t): ###|#######¦#######'#######
    """ ########|#######¦#######,#######`#######|#######|#######
    infut: (x, y): coorz
           (fgr, bgr): RGB colorz
           sgr: list
           t: text
    oufut: void
    xmple: Display(1,2,[10,150,230],[30,15,70],[1,3],'xa-xa')
    notes: void
    """ ########¦#######'#######|#######,#######¦#######'#######
    fgr = ClrStr(0, fgr) #      '       ¦       |       ¦
    bgr = ClrStr(1, bgr) #      `       .       |       '
    sgr = SgrStr(sgr) # |       |       |       |       ¦
    print(CSI + f'{y};{x}', end = 'H') #|       ¦       |
    print(CSI + fgr + bgr + sgr, end = 'm') #   |       |
    print(t) #  '       |       |       |       '       |     
    print(CSI, end = 'm') #     ¦       ¦       ¦       ¦
#       |       '       ¦       '       ¦       |       |
def Eraser(x, y, n): ###`#######|#######|#######|#######,#######
    """ ########|#######`#######¦#######¦#######`##Eraser#spec##




    """ ########'#######|#######'#######¦#######|#######,#######
    print(CSI + f'{y};{x}', end = 'H') #|       ¦       |
    print(CSI + str(n), end = 'X') #####.#######|##########cross
#       |       |       ¦       ¦       ¦       |       `
Bold = 1 #######¦#######|#######|#######|#######¦#######.#######
Ital = 3 #######,#######,#######|#######¦#######|#######¦#######
Norm = 22 ######¦#######.#######¦#######¦#######,#######|#######
class Brush: ###|#######¦#######'#######|#######'#######,#######
    def __init__(self, patron, répéter, sgr = [Norm]): #|
        if type(patron) is int: #       |       ¦       ,
            patron = hex(patron)[2:].upper() # convert to hex
            self.stroke = patron.rjust(répéter, ' ') #  |
        else: # |       |       ¦       ¦       ,       |
            self.stroke = patron * répéter #    |       ¦
        self.length = len(self.stroke) #,       ¦       |
        self.sgr = sgr #¦       '       ¦       |       ¦
    #   |       ¦       '       ,       :       |       ¦
    def rndm_sgr(self): #random#sgr#####¦#######'#######'#######
        ls = (Bold, Ital, Norm) #       |       '       | 
        self.sgr = sample(ls, randint(1, len(ls))) #    |
#       ¦       |       ¦       |       ,       `       '
scw = 3 # scv width     |       '       ;       ,       |
class Canvas: ##¦#######'#######|#######|#######'#######¦#######
    Red   = [200,   0,   0] #   '       ¦       ,       |
    Grey  = [120, 120, 100] #   ¦       |       ¦       ¦
    Blue  = [120, 120, 250] #   |       ,       |       :
    Green = [  0, 200,   0] #   ¦       '       |       ;
    State = [(50, 120, 30), (10, 30, 20)] #     '       ¦
    flat_03 = Brush('-', scw) # ,       .       ¦       |
    hexbrush_01 = [Brush(j, 1) for j in range(16)] #    '
    hexbrush_03 = [Brush(j, scw) for j in range(16)] #  '
    bar = Brush('¦', 1) #       ¦       |       |       |
    nscv = 10 # mx number of scvs in the waiting line   ¦
    width = 35 # canvas width   |       ¦       '       ¦
    def __init__(self, lift): # ¦       '       ¦  consa
        self.ORIG = (1 + lift.id * Canvas.width, 1) #   ¦
        self.lift = lift #      ¦       '       |       ¦
        self.Coorz = list(self.ORIG) #  `       |       |
        self.Clr = [Canvas.Grey[:], []] #       '       |
        for j in reversed(range(args.nfloors)): #       ¦
            self.DrawFloor(j) # |       ¦       |       |
        self.Clr[0] = Canvas.Red # draw initial floor position
        self.GetFloorCoorz(lift.floor) #`       ;       ¦
        self.Draw(Canvas.hexbrush_01[lift.floor]) #     |
        self.floor = lift.floor # last drawn floor position
        self.queue = deepcopy(self.lift.queue) #'       |
    #   |       |       ¦       '       |       |       ¦
    def Draw(self, brush): #    ¦       '       ¦       '
        Display(*self.Coorz, *self.Clr, brush.sgr, brush.stroke)
        self.Coorz[0] += brush.length # |       ¦       |
    #   '       ,       |       ¦       |       |       '
    def NewLine(self): #,       |       ¦       ,       ¦
        self.Coorz[0] = self.ORIG[0] #  |       .       :
        self.Coorz[1] += 1 #    :       '       `       .
    #   |       ¦       '       '       ¦       ¦       , 
    def DrawFloor(self, floor): #       '       :       ¦
        floor %= 16 # name floors only with hex numbers '
        self.Draw(Canvas.hexbrush_01[floor]) #  '       |
        for j in range(Canvas.nscv): #  '       |       ¦
            self.Draw(Canvas.flat_03) # ,       ¦       '
            self.Clr[0][2] += j*4 # make gradient       |
        self.Clr[0][2] = Canvas.Grey[2] # revert'       ;
        self.NewLine() #'       |       ¦       '       ¦ 
        self.Draw(Canvas.bar) # |       |       ¦       |
        self.NewLine() #,       |       ¦       |       |
    #   |       |       ¦       ¦       '       ¦       '
    def GetFloorCoorz(self, floor): #   |       '       ,
        """ ####|#######,#######|#######|#######¦#######|#######
        pozition ze cursor over floor name      |       '
        """ ####¦#######|#######,#######|#######¦#######¦#######
        self.Coorz[0] = self.ORIG[0] #  '       :       '
        self.Coorz[1] = 2 * (args.nfloors - floor) - 1 #'
    #   |       '       |       ;       |       ¦       |
    def DrawQueue(self, floor): #       ;       '       ¦
        self.Clr[0] = Canvas.Blue #     ¦       |       :
        self.GetFloorCoorz(floor) #     ,       ¦       |
        self.Coorz[0] += 1 #    ;       '       ;       ¦
        self.Coorz[1] += 1 #    ,       |       |       :
        for scv in self.lift.queue[floor]: #    '       ¦
            Canvas.hexbrush_03[scv.dest].rndm_sgr() #   |
            self.Draw(Canvas.hexbrush_03[scv.dest]) #   ¦
    #   ,       '       |       ¦       ;       |       '
    def EraseQueue(self, floor): #      '       |       ¦
        self.GetFloorCoorz(floor) #     ¦       '       ¦
        self.Coorz[0] += 1 #    :       '       |       :
        self.Coorz[1] += 1 #    ,       ;       ¦       |
        for scv in self.queue[floor]: # ¦       ,       '
            Eraser(*self.Coorz, scw) #  |       |       ¦
            self.Coorz[0] += scw #      ¦       |       ,
    #   ¦       |       '       |       ¦       |       ;
    def DumpState(self, clock): #       '       ,       .       `
        self.GetFloorCoorz(0) #
        self.Coorz[0] += 1 #         qq
        self.Coorz[1] += 3 #
        a = str(clock) #,       |       ¦       :       ¦ 
        b = self.lift.task.__str__() #  `       ¦       |
        c = ', '.join(map(lambda j: str(j), self.lift.exitstk))
        t = f'{a} [{b}] ❬❬{c}❭❭' #      ¦       |       ,
        Eraser(*self.Coorz, Canvas.width) #     ;       |
        Display(*self.Coorz, *Canvas.State, [Norm], t) #'
    #   |       ¦       ¦       '       :       |       ¦
    def Picture(self, clock): # :       '       :       '   
        self.Clr[0] = Canvas.Red # lift floor colour    :
        floor = self.lift.floor #       |       ¦       '
        self.GetFloorCoorz(floor) #     '       ;       |
        if floor != self.floor: # cmp with prev state   |
            self.Draw(Canvas.hexbrush_01[floor]) #      '
            self.Clr[0] = Canvas.Grey # revert  ;       '
            self.GetFloorCoorz(self.floor) #    |       ¦
            self.Draw(Canvas.hexbrush_01[self.floor]) # ¦
            self.NewLine() #    |       ¦       '       |
            self.Draw(Canvas.bar) #     '       |       ¦ 
        else: # |       ¦       '       ¦       ,       |     
            self.NewLine() #    ¦       |       :       ¦
            self.Clr[0] = Canvas.Green #|       ¦       ,
            self.Draw(Canvas.bar) #     '       |       :
        self.floor = floor # update last state  '       ;
        for j in range(args.nfloors): # |       ,       |
            if self.lift.queue[j] == self.queue[j]: #   |
                continue #      |       |       ¦       |
            if self.queue[j]: self.EraseQueue(j) #      '
            self.DrawQueue(j) # |       '       :       ¦
        self.queue = deepcopy(self.lift.queue) #|       ¦
        self.DumpState(clock) # '       ,       ¦       |
#>>>#############¡###################Ʌ####################dOthEMAtħ### 0
def dOthEMAth(): # main function     |                            |    1
    global args # declare some global|variables (actually only one]    2
    # ℘arser stuff ##################|############################|### 3
    pasa = argparse.ArgumentParser() # what is this?              |    4
    pasa.formatter_class = argparse.ArgumentDefaultsHelpFormatter #    5
    add_arg = pasa.add_argument # shorcut ######################¯##### 6
    add_arg("--lambda", type = float, default = .3, dest = 'λ', #      7
            help = "Poisson pdf parameter (--simula)") #######ɀ####### 8
    add_arg("--mode", type = int, default = 0, ####‰##########|####### 9
            help = "Com Center mode of operation") #          |        0
    add_arg('-n', type = int, default = 12, dest = 'ncycles', #        1
            help = "number of cycles (-1 for inf. loop)") #            2
    add_arg("--nfloors", type = int, default = 16, #######ʧ########### 3
            help = "number of floors") ##########@########|########### 4
    add_arg("--nlifts", type = int, default = 1, #        |            5
            help = "number of lifts") #########¼##########|########### 6
    add_arg("--simula", action = 'store_true', #          |            7
            help = "generate random users") #             |            8
    add_arg('-t', type = float, default = 2, dest = 'Δt', #            9
            help = "time in sec. between 2 clock ticks") #             0
    add_arg("--verbose", action = 'store_true', #                      1
            help = "debug info") ##############Ƚ###################### 2
    add_arg("--visual", action = 'store_true', #                       3
            help = "ze old hacker") #                                  4
    args = pasa.parse_args() #                                         5
    ### loℭal stuff ###########ǯ#################ș#################### 6
    regex = re.compile(r'\d+') #                 |                     7
    lift = [Lift(j) for j in range(args.nlifts)] #                     8
    clock = 0 ## ticß coünter ########á####ƨ########################## 9
    if args.visual: #   |             |    |                           0
        system("clear") #             |    |                           1
        print(CSI + '?25', end = 'l') # hidé cursor                    2
        canvas = [Canvas(j) for j in lift] #                           3
        log = open("lift.log", 'w') ##…############################### 4
        args.simula = True #          |                                5
    else: ###############ɸ#######################ɶ#########ɛ########## 6
        log = sys.stdout #                       |         |           7
    if args.verbose: log.write(str(args) + '\n') # <<<ƒoobll<<<<<<<<<< 8
    #############################Ǒ##### staät #############|########## 9
    while clock != args.ncycles: # let's ℊou               |          0
        if args.simula: # if True simulate requests by generating scvs 1
            gen_scv() #                                    |           2
        else: ###############ǣ############ read requests from ze infut 3
            get_infut(regex) #                             |           4
        assign(lift) # asign lift requests ################|########## 5
        for j in range(args.nlifts): ################⁇################ 6
            if args.visual: canvas[j].Picture(clock) #     |           7
            lift[j].cycle = False ###Ϡ#####################|########## 8
            while not lift[j].cycle: #                     |           9
                if args.verbose: #                         |           0
                    log.write(f"{clock}: {j} {lift[j]}\n") #           1
                lift[j].action() ##################################### 2
        time.sleep(args.Δt) # cycle time                               _
        clock += 1 # clcknext #################################### <<< _

def exit(code): ##################################✚################### 0
    if args.visual: print(CSI + '?25', end = 'h') # show cursor        1
    sys.exit(code) # _________________________________________________ 2

if __name__ == '__main__':
    try:
        dOthEMAth()
        exit(0)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        exit(1)
##µ®×―############################################################# log:
