import math, os, glob
from PIL import Image, ImageDraw, ImageFilter
RES='android/app/src/main/res'
GOLD2=(255,211,107); CRIMSON=(220,20,60); GOLD=(232,181,58)
def lerp(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))

def dial(size, scale=1.0, bg=None, radius_frac=0.0):
    S=size*4
    im=Image.new('RGBA',(S,S),(0,0,0,0) if bg is None else bg+(255,))
    if bg is not None and radius_frac>0:
        mask=Image.new('L',(S,S),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,S-1,S-1],radius=int(S*radius_frac),fill=255)
        im.putalpha(mask)
    d=ImageDraw.Draw(im)
    c=S/2; R=S*0.40*scale
    # glow
    glow=Image.new('RGBA',(S,S),(0,0,0,0)); g=ImageDraw.Draw(glow)
    g.ellipse([c-R*0.9,c-R*0.9,c+R*0.9,c+R*0.9],outline=CRIMSON+(150,),width=int(S*0.05*scale))
    glow=glow.filter(ImageFilter.GaussianBlur(S*0.04*scale))
    im.alpha_composite(glow)
    d=ImageDraw.Draw(im)
    n=48; used=0.72
    for i in range(n):
        a=i/n*2*math.pi-math.pi/2
        major=i%6==0
        r1=R; r2=R*(0.80 if major else 0.87)
        lit=(i+.5)/n<=used
        col=lerp(GOLD2,CRIMSON,i/(n*used)) if lit else (70,66,60)
        w=int(S*(0.022 if major else 0.014)*scale)
        d.line([(c+r1*math.cos(a),c+r1*math.sin(a)),(c+r2*math.cos(a),c+r2*math.sin(a))],fill=col+(255,),width=w)
    # inner ring track + arc
    rr=R*0.62; w=int(S*0.06*scale)
    d.ellipse([c-rr,c-rr,c+rr,c+rr],outline=(40,38,36,255),width=w)
    d.arc([c-rr,c-rr,c+rr,c+rr],start=-90,end=-90+250,fill=GOLD+(255,),width=w)
    # cap rounding
    for ang in (-90,-90+250):
        a=math.radians(ang); x=c+(rr-w/2)*math.cos(a); y=c+(rr-w/2)*math.sin(a)
        d.ellipse([x-w/2,y-w/2,x+w/2,y+w/2],fill=GOLD+(255,))
    # marker
    a=used*2*math.pi-math.pi/2; mr=R*0.72*1.0; m=S*0.035*scale
    # center dot
    cd=S*0.075*scale
    d.ellipse([c-cd,c-cd,c+cd,c+cd],fill=CRIMSON+(255,))
    return im.resize((size,size),Image.LANCZOS)

dens={'mdpi':1,'hdpi':1.5,'xhdpi':2,'xxhdpi':3,'xxxhdpi':4}
for k,f in dens.items():
    p=f'{RES}/mipmap-{k}'
    dial(int(48*f),scale=1.0,bg=(0,0,0),radius_frac=0.22).save(f'{p}/ic_launcher.png')
    # round legacy
    im=dial(int(48*f),scale=1.0,bg=(0,0,0)); mask=Image.new('L',im.size,0); ImageDraw.Draw(mask).ellipse([0,0,im.size[0]-1,im.size[1]-1],fill=255); im.putalpha(mask); im.save(f'{p}/ic_launcher_round.png')
    dial(int(108*f),scale=0.62).save(f'{p}/ic_launcher_foreground.png')
open(f'{RES}/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#000000</color>\n</resources>\n')
# splash screens: black with dial
for f in glob.glob(f'{RES}/drawable*/splash.png'):
    w,h=Image.open(f).size
    im=Image.new('RGBA',(w,h),(0,0,0,255)); s=int(min(w,h)*0.32)
    im.alpha_composite(dial(s,scale=1.0),((w-s)//2,(h-s)//2)); im.convert('RGB').save(f)
dial(1024,bg=(0,0,0),radius_frac=0.22).save('resources/icon-preview.png')
print('ok')
