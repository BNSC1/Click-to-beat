import numpy as np, matplotlib.pyplot as plt, pygame
np.set_printoptions(threshold=np.inf)
#pip install pygame 

# Setup
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode([640,200]);fps=60 # Display
cursorcolor=(160,160,255);black=(0,0,0);errorbarcolor=(255,255,255);lastcursorcolor=(80,80,128);bestcursorcolor=(0,128,0)
screen.fill(black)
pygame.display.set_caption(u'Bootleg osu! GA')
isPlaying=True;auto=True;hispeed=False;isHit=False
clk=pygame.time.Clock()
cursor_pos=cursor_startpos=40
best_hiterror=99999; hiterror_sum=0;hiterror=0;best_cursor=-999
# Font
font_color=(255,255,255);font=pygame.font.SysFont('System Bold',24)
def showFont( text, x, y, font=font, color=font_color):
    global screen
    text = font.render(text, 1, color)
    screen.blit( text, (x,y))
def drawErrorbar():
    global errorbarcolor
    pygame.draw.rect(screen,errorbarcolor,(40,70,5,50))
    pygame.draw.rect(screen,errorbarcolor,(590,70,5,50))
    pygame.draw.rect(screen,errorbarcolor,(40,90,550,5))
    pygame.draw.rect(screen,errorbarcolor,(315,60,5,70))
# Sound
hitsound=pygame.mixer.Sound('sounds/hit.wav')

def showTrainrate():
    plt.clf()
    plt.plot(best_fitness_array)    
    plt.grid()
    plt.title('Train Rate')
    plt.ylabel('Hiterror')
    plt.xlabel('Generation')
    plt.pause(0.001)
def loopRound():
    global chromosome, generation ,fitness_array, best_fitness_array, best_hiterror, hitcursor_array,hiterror,cursorcolor,best_cursor
    if hiterror<best_hiterror: best_hiterror=hiterror;best_cursor=population[chromosome]
    fitness_array.append(hiterror)
    chromosome+=1
    if chromosome>chromosome_num-1:
        nextG()
        best_fitness_array.append(best_hiterror)
        fitness_array=[]
        chromosome=0
        generation+=1
        showTrainrate()
showhiterror = -1
def loopGame():
    global auto,isPlaying,hispeed, cursor_pos,fps,screen,black, hiterror, showhiterror,cursor,bestcursor
    while isPlaying:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: isPlaying=False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: isPlaying=False
                elif event.key==pygame.K_a:
                    if auto==True: hispeed=True;fps=600000
                elif event.key==pygame.K_d:
                    if hispeed==True: hispeed=False;fps=60

        cursor_pos+=6
        if population[chromosome] == cursor_pos:
            hitsound.play()
            hiterror = abs(population[chromosome] - 315)
            cursor_lastpos=population[chromosome]
            showhiterror = 0
        if cursor_pos>592: 
            cursor_pos=cursor_startpos
            loopRound()

        if 0 <= showhiterror < 60:
            
            showFont(u'hiterror: '+str(hiterror)+u', best hiterror: '+str(best_hiterror),380,160)  #顯示得分
            showhiterror += 1
            pygame.draw.rect(screen,lastcursorcolor,(cursor_lastpos,70,5,50))
            if showhiterror == 60: showhiterror = -1
        #Cursor
        pygame.draw.rect(screen,cursorcolor,(cursor_pos,70,5,50))
        pygame.draw.rect(screen,bestcursorcolor,(best_cursor,70,5,50))
        pygame.display.update()
        screen.fill(black)
        drawErrorbar()
        
        showFont(u'Generation '+str(generation)+', Chromosome '+str(chromosome)+u', A to speed up, D to slow down' ,18,10)
    
        clk.tick(fps)
# set_volume
def set_all_volume(v):  #0~1
    global hitsound
    hitsound.set_volume(v)

#GA
chromosome = 0
chromosome_num = 10
population = np.array([0]*chromosome_num)
generation = 0
fitness_array = []
best_fitness_array = []
sel_num = round(chromosome_num*0.3)
copy_num = chromosome_num - sel_num
for i in range(chromosome_num):
    population[i] = np.random.choice(np.arange(40,592,6))
def nextG():
    global population
    #Selection
    sel_idx = np.argsort(fitness_array)[:sel_num]
    tmppopulation = np.copy(population[sel_idx])
    #copy
    for i in range(copy_num):
        copy_idx = np.random.choice(sel_idx)
        tmppopulation = np.concatenate((tmppopulation, population[copy_idx].reshape(1)),axis=0)
    population = np.copy(tmppopulation)
    #Crossover，將某一下的某一個軸和其他chromosome的同一下的同一軸互換
    for i in range(sel_num, chromosome_num):    #最好的那幾次不動
        if np.random.rand() < 0.3:
            change_chromosome = np.random.randint(sel_num, chromosome_num) #最好的那幾次不換
            while i == change_chromosome: change_chromosome = np.random.randint(sel_num, chromosome_num) #選到自己重選
            #swap
            tmp = np.copy(population[i])
            population[i] = np.copy(population[change_chromosome])
            population[change_chromosome] = np.copy(tmp)
    #Mutation
    for i in range(sel_num, chromosome_num):    #最好的那幾次不動
        if np.random.rand() < 0.3:
            population[i] = np.random.choice(np.arange(40,592,6))
set_all_volume(0.1)
loopGame()
pygame.quit()
quit()