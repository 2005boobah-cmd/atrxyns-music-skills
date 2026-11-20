import math,random
import numpy as np
from PIL import Image,ImageDraw,ImageOps,ImageChops,ImageFilter

class BadgeEffects:
    def __init__(self,width,height,logo=None,accent_color=None):
        import re,colorsys
        from PIL import ImageColor
        if accent_color is not None and (not isinstance(accent_color,str) or not re.fullmatch(r"#[0-9a-fA-F]{6}",accent_color)):
            raise ValueError("accent_color must be a six-digit hex color, e.g. #719EB2")
        self.accent_hsv=colorsys.rgb_to_hsv(*(v/255 for v in ImageColor.getrgb(accent_color))) if accent_color else None
        self.width,self.height=width,height
        self.x,self.y,self.radius=(width*.465,height*.42,width*.245) if height>width else (width*.5,height*.40,height*.245)
        logo=logo or str(__import__('pathlib').Path(__file__).resolve().parent.parent/'assets/NFM_Brand_Emblem.png')
        self.logo=Image.open(logo).convert('RGBA')
        self.level=np.zeros(56);self.speed=np.zeros(56);self.last=None;self.flow=0.;self.burst=0.
        grid=np.linspace(-2.05,2.05,420,dtype=np.float32)
        yy,xx=np.meshgrid(grid,grid,indexing='ij');self.r=np.hypot(xx,yy);self.a=np.arctan2(yy,xx)
        rng=random.Random(82)
        self.sparks=[(rng.random()*math.tau,rng.random(),rng.uniform(.6,1.5),rng.uniform(.6,1.5)) for _ in range(100)]
        self.cache={}
        self.particle_impulse=0.;self.oldkick=0.
    def frame(self,values,time,bass=0.,kick=0.,voice=0.,treble=0.):
        dt=1/24 if self.last is None else min(.1,max(1/120,time-self.last));self.last=time
        self.flow+=dt*(.45+1.8*bass+3.2*kick)
        self.burst=max(kick,self.burst*math.exp(-dt*8))
        # Different spectral regions drive different points, with a damped spring response.
        vals=np.asarray(values);shift=(time*.012)%1
        target=np.interp((np.linspace(0,1,56,endpoint=False)+shift)%1,np.linspace(0,1,57),np.r_[vals,vals[0]])*(.35+.65*bass)
        self.speed+=(target-self.level)*100*dt;self.speed*=math.exp(-dt*12);self.level+=self.speed*dt
        a=self.a;r=self.r;phase=(a/math.tau+1)%1
        angular=np.interp(phase,np.linspace(0,1,57),np.r_[self.level,self.level[0]])
        lobes=(.5+.5*np.sin(7*a+self.flow))*(.45+.55*np.sin(11*a-self.flow*.8)**2)
        reach=.055+.30*bass+.36*self.burst+.24*angular+.15*voice*lobes
        dist=np.maximum(0,r-1)
        curl=.035*np.sin(13*a-9*dist+self.flow*2)+.018*np.sin(23*a+22*dist-self.flow*1.4)
        fingers=(.5+.5*np.sin(9*a+self.flow*.65+1.3*np.sin(3*a-self.flow*.23)))**5
        tip=1+reach*(.32+.54*lobes+.52*fingers)
        width=.025+.052*bass+.035*angular
        plume=np.exp(-((r-tip+curl)/width)**2)
        root=np.exp(-dist/(.05+reach*.65))
        texture=np.clip(.5+.3*np.sin(17*a-35*dist+self.flow*3)+.2*np.sin(29*a+19*dist-self.flow*2),0,1)
        gaps=.35+.65*(.5+.5*np.sin(9*a+self.flow*.7))
        outer=np.exp(-((r-tip-.065-.035*np.sin(6*a+self.flow))/(width*1.8))**2)*texture*.24
        filaments=np.exp(-((r-1.02-reach*(.3+.9*fingers)+.03*np.sin(21*a+dist*29-self.flow*2))/.019)**2)*fingers
        density=((root*.58+plume*1.05)*(.30+.70*texture)+outer+filaments*.6)*gaps
        density*=np.clip((r-.995)/.018,0,1)*np.clip((1.93-r)/.18,0,1)
        silver=np.clip(.5+.5*np.sin(3*a-self.flow*.16),0,1)**3
        rgb=np.zeros((*r.shape,3),dtype=np.uint8)
        for c,(red,metal) in enumerate(zip((218,22,49),(199,198,205))):rgb[:,:,c]=(red*(1-silver)+metal*silver).astype(np.uint8)
        alpha=np.clip(density*(180+60*bass+60*self.burst),0,245).astype(np.uint8)
        size=round(self.radius*4.1)
        smoke=Image.fromarray(np.dstack((rgb,alpha))).resize((size,size),Image.Resampling.BICUBIC)
        image=Image.new('RGBA',(self.width,self.height))
        halo=smoke.filter(ImageFilter.GaussianBlur(self.height*.008))
        halo.putalpha(halo.getchannel('A').point(lambda x:round(x*.32)))
        image.alpha_composite(halo,(round(self.x-size/2),round(self.y-size/2)))
        image.alpha_composite(smoke,(round(self.x-size/2),round(self.y-size/2)))
        # Thin silver curls follow the midrange separately from the bass plumes.
        detail=np.exp(-((r-1.025-(.05+.16*voice+.06*self.burst)*(.5+.5*np.sin(8*a-self.flow*1.8))+.019*np.sin(27*a+dist*50-self.flow*3))/.012)**2)
        detail*=np.clip((r-1)/.025,0,1)*(.25+.75*voice)*gaps
        va=np.clip(detail*170,0,190).astype(np.uint8);vr=np.full((*r.shape,3),(210,207,210),dtype=np.uint8)
        mist=Image.fromarray(np.dstack((vr,va))).resize((size,size),Image.Resampling.BICUBIC);image.alpha_composite(mist,(round(self.x-size/2),round(self.y-size/2)))
        self.particle_impulse=self.particle_impulse*math.exp(-dt*5)+max(0,kick-self.oldkick)*.16
        self.oldkick=kick
        d=ImageDraw.Draw(image)
        for i,(ang,seed,speed,scale) in enumerate(self.sparks):
            age=(seed+self.flow*speed*.13)%1
            angle=ang+.12*math.sin(self.flow+seed*20)
            radius=self.radius*(1.07+age*1.25+self.particle_impulse)
            x=self.x+math.cos(angle)*radius;y=self.y+math.sin(angle)*radius
            if y>self.height*.76 or y<12:continue
            fade=(1-age)**.65
            opacity=round((165+90*max(treble,self.burst))*fade)
            rad=max(1,self.height*.0018*scale*(1+.7*self.burst))
            # Dark keyline + bright core remain legible over practical lights and shadows.
            d.ellipse((x-rad-2,y-rad-2,x+rad+2,y+rad+2),fill=(2,2,7,round(opacity*.85)))
            color=(245,221,218,opacity) if i%3==0 else (239,65,82,opacity)
            d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=color)
            trail=(4+24*self.burst+10*treble)*scale
            for j in range(4,0,-1):
                d.line((x-math.cos(angle)*trail*(j-1)/4,y-math.sin(angle)*trail*(j-1)/4,x-math.cos(angle)*trail*j/4,y-math.sin(angle)*trail*j/4),fill=(*color[:3],round(opacity*(1-j/5)*.65)),width=max(1,round(rad*.65)))
            if i%3==0:d.ellipse((x-.65,y-.65,x+.65,y+.65),fill=(255,244,239,opacity))
        diameter=round(self.radius*1.97)
        if diameter not in self.cache:
            logo=ImageOps.fit(self.logo,(diameter,diameter),method=Image.Resampling.LANCZOS)
            mask=Image.new('L',(diameter,diameter));ImageDraw.Draw(mask).ellipse((0,0,diameter-1,diameter-1),fill=255);logo.putalpha(ImageChops.multiply(logo.getchannel('A'),mask));self.cache[diameter]=logo
        image.alpha_composite(self.cache[diameter],(round(self.x-diameter/2),round(self.y-diameter/2)))
        d=ImageDraw.Draw(image);rad=self.radius
        for i in range(12):
            theta=i*math.tau/12+.17*math.sin(time*.8+i)
            energy=float(self.level[(i*4)%56])
            if energy>.15:
                start=math.degrees(theta);box=(self.x-rad-3,self.y-rad-3,self.x+rad+3,self.y+rad+3)
                d.arc(box,start,start+4+8*energy,fill=(245,135,148,round(90+130*energy)),width=max(2,round(self.height*.003)))
        d.ellipse((self.x-rad-2,self.y-rad-2,self.x+rad+2,self.y+rad+2),outline=(5,5,9,255),width=5)
        d.ellipse((self.x-rad,self.y-rad,self.x+rad,self.y+rad),outline=(213,211,216,255),width=max(2,round(self.height*.002)))
        if self.accent_hsv is not None:
            # Recolor the branding and graphics together; keep original PNG, alpha,
            # neutral chrome and the fixed silver border unchanged.
            rgba=np.asarray(image).copy()
            hsv=np.asarray(image.convert('RGB').convert('HSV')).copy()
            red=((hsv[:,:,0]<30)|(hsv[:,:,0]>225))&(hsv[:,:,1]>45)&(rgba[:,:,3]>0)
            hue,saturation,_=self.accent_hsv
            hsv[:,:,0][red]=round(hue*255)
            hsv[:,:,1][red]=np.clip(hsv[:,:,1][red].astype(float)*max(.12,saturation)/.82,0,255).astype(np.uint8)
            tinted=np.asarray(Image.fromarray(hsv,'HSV').convert('RGB'))
            rgba[:,:,:3][red]=tinted[red]
            image=Image.fromarray(rgba,'RGBA')
        return image
