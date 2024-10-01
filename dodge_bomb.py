import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
        pg.K_DOWN:(0,+5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(+5,0)
        }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとん　または　爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue　画面内ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate
def gameover(screen:pg.Surface) -> None:
    """
    引数　screnn=画面全体
    戻り値　None
    """
    enn = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(enn, (0,0,0),pg.Rect(0,0,WIDTH, HEIGHT))
    enn.set_alpha(200)
    screen.blit(enn,[0,0])
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",
            True, (255,255,255))
    screen.blit(txt, [300, 300])
    img = pg.image.load("fig/8.png")
    enn = pg.Surface((20,20))
    pg.draw.circle(enn, (0,0,0),(10,10),10)
    screen.blit(img,[300,200])
    pg.display.update()
    time.sleep(5)
def kakudai() -> None:
    """
    引数　None
    戻り値　imgs, accs
    """
    accs = [a for a in range(1,11)]
    imgs = list()
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
        imgs.append(bb_img)
    
        # avx = vx*bb_accs[min(tmr//500,9)]
        # bb_img = bb_imgs[min(tmr//500,9)]
    return imgs, accs
def kirikae():
    print()


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  #空のsurface
    bb_img.set_colorkey((0,0,0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = kakudai()
    while True:
        avx = vx*bb_accs[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500,9)]
        bb_rct = bb_img.get_rect(center=bb_rct.center)     

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾重なり
            gameover(screen)
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
         #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
         #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #   sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #   sum_mv[0] += 5

        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip((vx, vy))
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
