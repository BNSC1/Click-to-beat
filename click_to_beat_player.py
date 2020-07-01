import numpy as np, math, matplotlib.pyplot as plt, pygame
np.set_printoptions(threshold=np.inf)
#pip install pygame 

# Setup
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode([640,200]);fps=360 #Display
cursorcolor=(160,160,255);black=(0,0,0);errorbarcolor=(255,255,255);lastcursorcolor=(80,80,128);bestcursorcolor=(0,128,0)
screen.fill(black)
pygame.display.set_caption(u'Bootleg osu!')
isPlaying=True;isHit=False
clk=pygame.time.Clock()
cursor_pos=cursor_startpos=40
best_hiterror=99999; hiterror_sum=0;hiterror=0;best_cursor=-999;last_cursor=-999
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
def hit():
    global isHit,best_hiterror,hiterror,best_cursor,last_cursor
    if isHit==False:
        hitsound.play()
        hiterror = abs(cursor_pos - 315)
        last_cursor=cursor_pos
        if hiterror<best_hiterror: best_hiterror=hiterror;best_cursor=cursor_pos
        isHit=True
def loopRound():
    global isHit
    isHit=False
showhiterror = -1
def loopGame():
    global auto,isPlaying,hispeed, cursor_pos,fps,screen,black, hiterror, showhiterror,cursor,bestcursor,last_cursor
    while isPlaying:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: isPlaying=False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: isPlaying=False
                elif event.key==pygame.K_x: hit()
        cursor_pos+=1
        showhiterror = 0
        if cursor_pos>592: 
            cursor_pos=cursor_startpos
            loopRound()
        if 0 <= showhiterror < 60:
            
            showFont(u'hiterror: '+str(hiterror)+u', best hiterror: '+str(best_hiterror),380,160)  #顯示得分
            showhiterror += 1
            pygame.draw.rect(screen,lastcursorcolor,(last_cursor,70,5,50))
            if showhiterror == 60: showhiterror = -1
        #Cursor
        pygame.draw.rect(screen,cursorcolor,(cursor_pos,70,5,50))
        pygame.draw.rect(screen,bestcursorcolor,(best_cursor,70,5,50))
        pygame.display.update()
        screen.fill(black)
        drawErrorbar()
        showFont(u'X to beat!' ,18,10)
        clk.tick(fps)
# set_volume
def set_all_volume(v):  #0~1
    global hitsound
    hitsound.set_volume(v)
set_all_volume(0.1)
loopGame()
pygame.quit()
quit()