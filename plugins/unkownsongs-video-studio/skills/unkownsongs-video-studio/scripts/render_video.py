#!/usr/bin/env python3
"""Render cinematic scenic music videos with a rounded, glowing audio spectrum."""
import argparse, hashlib, json, math, os, random, shutil, subprocess, sys
from pathlib import Path

def ffmpeg_path(explicit=None):
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.is_file(): raise ValueError("FFmpeg path does not exist")
        return str(p)
    found = shutil.which("ffmpeg")
    if found: return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as e:
        raise RuntimeError("Install FFmpeg or imageio-ffmpeg in this task environment") from e

def run(cmd, **kw):
    result = subprocess.run([str(x) for x in cmd], capture_output=True, **kw)
    if result.returncode:
        msg = result.stderr.decode(errors="replace") if isinstance(result.stderr, bytes) else result.stderr
        raise RuntimeError(msg[-6000:])
    return result.stdout

def read_project(path, ff):
    import numpy as np
    p = Path(path).resolve()
    cfg = json.loads(p.read_text(encoding="utf-8-sig"))
    root = p.parent
    for key in ("font", "font_bold"):
        if cfg.get(key): cfg[key] = str((root / cfg[key]).resolve())
    def local(v):
        if not isinstance(v, str) or "://" in v: raise ValueError("Use actual local file paths")
        q = (root / v).resolve()
        if not q.is_file(): raise ValueError(f"Missing local asset: {q}")
        return q
    if cfg.get("layout", "badge") not in ("badge", "ribbon"):
        raise ValueError("Use layout badge or ribbon")
    if not cfg.get("logo"):
        cfg["logo"] = str(Path(__file__).resolve().parent.parent / "assets" / "NFM_Brand_Emblem.png")
    if cfg.get("logo"):
        from PIL import Image
        cfg["logo"] = str(local(cfg["logo"]))
        with Image.open(cfg["logo"]) as logo:
            logo.verify()
    audio = local(cfg["audio"])
    raw = run([ff, "-v", "error", "-i", audio, "-f", "f32le", "-ac", "1", "-ar", "22050", "pipe:1"])
    wave = np.frombuffer(raw, dtype=np.float32)
    duration = len(wave) / 22050
    if duration <= 0: raise ValueError("Audio is empty")
    w, h, fps = int(cfg.get("width",1920)), int(cfg.get("height",1080)), int(cfg.get("fps",24))
    if w < 320 or h < 320 or w % 2 or h % 2 or fps not in (24,25,30,60):
        raise ValueError("Use even dimensions >=320 and 24/25/30/60 fps")
    scenes = cfg.get("scenes", [])
    if not scenes: raise ValueError("Provide real scenic images or video clips")
    has = ["duration" in s for s in scenes]
    if any(has) and not all(has): raise ValueError("Provide all scene durations or none")
    each = duration / len(scenes); normalized = []; cursor = 0.
    for s in scenes:
        d = float(s.get("duration",each))
        if not math.isfinite(d) or d <= 0: raise ValueError("Scene durations must be positive")
        normalized.append({**s,"path":local(s["file"]),"start":cursor,"duration":d})
        cursor += d
    if abs(cursor-duration) > .15: raise ValueError(f"Scene duration {cursor:.2f}s differs from song {duration:.2f}s")
    normalized[-1]["duration"] += duration-cursor
    cues = []
    if cfg.get("lyrics"):
        cues = json.loads(local(cfg["lyrics"]).read_text(encoding="utf-8-sig"))
        if not isinstance(cues,list): raise ValueError("Lyrics JSON must be a cue array")
        last = -1
        for i,c in enumerate(cues):
            if c.get("needs_review"): raise ValueError(f"Review lyric cue {i} before exporting")
            a,b = c.get("start"),c.get("end")
            if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or not math.isfinite(a+b):
                raise ValueError(f"Missing/invalid timing in lyric cue {i}")
            if a < 0 or b <= a or b > duration+.1 or a < last-.01:
                raise ValueError(f"Out-of-order, overlapping or out-of-range lyric cue {i}")
            if not str(c.get("text","")).strip(): raise ValueError(f"Empty lyric cue {i}")
            if len(str(c["text"]).splitlines())>2: raise ValueError(f"Lyric cue {i} exceeds two lines")
            last=b
    return p,cfg,audio,wave,duration,w,h,fps,normalized,cues

def font_path(value,bold=False):
    from PIL import ImageFont
    candidates = [value] if value else []
    candidates += [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"]
    for f in candidates:
        if f and Path(f).is_file():
            ImageFont.truetype(str(f),24)
            return Path(f).resolve()
    raise ValueError("Provide actual regular and bold font files")

def timestamp(v, srt=False):
    rate=1000 if srt else 100
    t=max(0,round(v*rate))
    if srt:return f"{t//3600000:02d}:{t//60000%60:02d}:{t//1000%60:02d},{t%1000:03d}"
    return f"{t//360000}:{t//6000%60:02d}:{t//100%60:02d}.{t%100:02d}"

def wrap_line(text,font,maxwidth):
    result=[]
    for para in text.splitlines():
        line=""
        for word in para.split():
            candidate=(line+" "+word).strip()
            if font.getlength(candidate)>maxwidth:
                if not line:raise ValueError("An unbreakable lyric word exceeds safe width")
                result.append(line);line=word
            else:line=candidate
        if line:result.append(line)
    if len(result)>2:raise ValueError(f"Split this lyric into shorter timed cues: {text}")
    return result

def escape_ass(text):
    return "".join("\\" + chr(0x2060) if c == "\\" else "\\{" if c == "{" else "\\}" if c == "}" else c for c in text)

def prepare_type(work,cfg,cues,w,h,start,duration):
    from PIL import ImageFont,Image,ImageDraw
    import numpy as np
    portrait=h>w
    unit=min(w,h)/1080
    regular=font_path(cfg.get("font"));bold=font_path(cfg.get("font_bold"),True)
    fonts=work/"fonts";fonts.mkdir(exist_ok=True)
    for f in {regular,bold}:shutil.copyfile(f,fonts/f.name)
    family=ImageFont.truetype(str(regular),24).getname()[0]
    boldfamily=ImageFont.truetype(str(bold),24).getname()[0]
    cx=w*(.47 if portrait else .5)
    badge = cfg.get("layout", "badge") == "badge"
    lyric_y = h * ((.69 if portrait else .83) if badge else (.70 if portrait else .79))
    safe=w*(.74 if portrait else .86)
    sizes=((72 if portrait else 65) if badge else (56 if portrait else 54))*unit
    font=ImageFont.truetype(str(regular),max(12,round(sizes)))
    fontb=ImageFont.truetype(str(bold),max(12,round(sizes*1.06)))
    lyric_color = "&H00FFFFFF" if badge else "&H00E6EEF3"
    shadow = unit * (3.5 if badge else 1)
    header=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,{family},{sizes:.1f},{lyric_color},{lyric_color},&H00170B08,&H70000000,0,0,0,0,100,100,0,0,1,{unit*1.8:.1f},{shadow:.1f},5,0,0,0,1
Style: Chorus,{boldfamily},{sizes*1.06:.1f},&H00C4E0FA,&H00C4E0FA,&H00170B08,&H70000000,-1,0,0,0,100,100,0,0,1,{unit*1.8:.1f},{unit:.1f},5,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass=header;srt=[];count=0
    for c in cues:
        a=max(start,c["start"]);b=min(start+duration,c["end"])
        if b<=a:continue
        text=str(c["text"])
        chorus=not badge and c.get("chorus",text.upper()==text and any(x.isalpha() for x in text))
        cue_font = fontb if chorus else font
        override = ""
        for size in range(cue_font.size, max(8, round(sizes*.58))-1, -2):
            try:
                lines = wrap_line(text, cue_font.font_variant(size=size), safe)
                override = rf"\fs{size}" if size != cue_font.size else ""
                break
            except ValueError:
                if not badge:
                    raise
        else:
            raise ValueError(f"Split this lyric into shorter timed cues: {text}")
        display=r"\N".join(escape_ass(line) for line in lines)
        ass+=f"Dialogue: 0,{timestamp(a-start)},{timestamp(b-start)},{'Chorus' if chorus else 'Lyric'},,0,0,0,,{{\\an5\\pos({cx:.0f},{lyric_y:.0f})\\fad(120,120){override}}}{display}\n"
        count+=1;srt.append(f"{count}\n{timestamp(a-start,True)} --> {timestamp(b-start,True)}\n"+'\n'.join(lines)+"\n")
    (work/"captions.ass").write_text(ass,encoding="utf-8-sig")
    (work/"captions.srt").write_text("\n".join(srt),encoding="utf8")
    # Readable lower gradient and understated brand, with no heavy caption box.
    yy,xx=np.mgrid[0:h,0:w]
    lower = np.clip((yy/h-(.69 if badge and not portrait else .55 if badge else .40))/.45,0,1)*(155 if badge else 175)
    edge=np.clip((((xx/w-.5)*2)**2+((yy/h-.48)*1.1)**2-.25)*50,0,70)
    alpha=np.clip(lower+edge,0,225).astype(np.uint8)
    plate=np.zeros((h,w,4),dtype=np.uint8);plate[:,:,:3]=(8,11,23);plate[:,:,3]=alpha
    im=Image.fromarray(plate)
    if badge:
        if not cfg.get('dynamic_logo'):
            draw_badge(im, cfg, regular)
        im.save(work/"overlay.png")
        return
    d=ImageDraw.Draw(im)
    bf=ImageFont.truetype(str(bold),max(14,round((40 if portrait else 37)*unit)))
    tf=ImageFont.truetype(str(regular),max(12,round((23 if portrait else 24)*unit)))
    def center(y,text,f,fill):
        text=str(text)
        if f.getlength(text)>safe:raise ValueError("Brand/title too wide; shorten title or adjust type")
        d.text((cx-f.getlength(text)/2,y),text,font=f,fill=fill,stroke_width=max(1,round(unit)),stroke_fill=(8,11,23,100))
    center(h*(.095 if portrait else .055),cfg.get("brand","Nox FM"),bf,(243,238,230,245))
    center(h*(.135 if portrait else .105),cfg.get("title",""),tf,(228,224,236,225))
    im.save(work/"overlay.png")

def fingerprint(path,settings):
    digest=hashlib.sha256(json.dumps(settings,sort_keys=True).encode())
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):digest.update(chunk)
    return digest.hexdigest()[:20]

def scenic_track(ff,work,scenes,w,h,fps,start,duration):
    end=start+duration;clips=[]
    images={".jpg",".jpeg",".png",".webp",".bmp",".tif",".tiff"}
    for i,s in enumerate(scenes):
        a=max(start,s["start"]);b=min(end,s["start"]+s["duration"])
        if b<=a:continue
        dur=b-a;count=math.ceil(dur*fps);source=s["path"]
        image=source.suffix.lower() in images
        settings={"w":w,"h":h,"fps":fps,"duration":dur,"offset":a-s["start"],"image":image,"v":1}
        name=work/f"scene_{fingerprint(source,settings)}.mp4"
        if not name.is_file():
            pre=[ff,"-y","-v","error"]
            if image:
                pre+=["-loop","1","-framerate",str(fps),"-i",source]
                z=f"1+0.035*on/{max(1,count)}"
                vf=f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={w}x{h}:fps={fps}"
            else:
                pre+=["-stream_loop","-1","-ss",str(a-s["start"]),"-i",source]
                vf=f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps}"
            fade=min(.3,dur/5)
            vf+=f",setsar=1,fade=t=in:st=0:d={fade},fade=t=out:st={max(0,dur-fade)}:d={fade}"
            run(pre+["-vf",vf,"-frames:v",count,"-an","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",name])
        clips.append(name)
        print(json.dumps({"stage":"scenes","finished":len(clips),"scene":i+1}),flush=True)
    # Cache files have controlled, apostrophe-free names in this work directory.
    (work/"concat.txt").write_text("\n".join("file '"+p.name+"'" for p in clips),encoding="utf8")
    out=work/"scenic.mp4"
    run([ff,"-y","-v","error","-f","concat","-safe","0","-i","concat.txt","-c","copy",out.name],cwd=work)
    return out

def analyze(wave,fps,start,duration,bands=56):
    import numpy as np
    n=math.ceil(duration*fps);size=2048;rate=22050
    edges=np.geomspace(3,size//2,bands+1).astype(int)
    window=np.hanning(size);spectrum=[]
    # Use a global reference across the original song, not per-frame or per-preview.
    refs=[]
    for t in np.linspace(0,max(0,len(wave)/rate-.1),min(1200,max(1,len(wave)//512))):
        pos=int(t*rate);seg=wave[pos:pos+size]
        if len(seg)<size:seg=np.pad(seg,(0,size-len(seg)))
        refs.append(np.abs(np.fft.rfft(seg*window)))
    reference=np.percentile(np.asarray(refs),96,axis=0)
    bandref=np.array([np.sqrt(np.mean(reference[a:max(a+1,b)]**2)) for a,b in zip(edges[:-1],edges[1:])])
    # Global band-aware calibration; an energy gate retains quiet-section dynamics.
    rmsref=max(1e-7,float(np.percentile(np.sqrt(np.mean(np.asarray([wave[k:k+512] for k in range(0,max(1,len(wave)-512),512)])**2,axis=1)),96))) if len(wave)>512 else 1
    for i in range(n):
        pos=int((start+i/fps)*rate);seg=wave[pos:pos+size]
        if len(seg)<size:seg=np.pad(seg,(0,size-len(seg)))
        fft=np.abs(np.fft.rfft(seg*window))
        energy=np.array([np.sqrt(np.mean(fft[a:max(a+1,b)]**2)) for a,b in zip(edges[:-1],edges[1:])])
        gate=min(1,float(np.sqrt(np.mean(seg*seg)))/rmsref)
        values=np.clip(np.log1p(energy/(bandref+.01)*2.5)/math.log(3.5),0,1)*gate**.55
        spectrum.append(values)
    smoothed=np.zeros(bands);result=[]
    for values in spectrum:
        smoothed+=np.where(values>smoothed,.65,.12)*(values-smoothed)
        result.append(smoothed.copy())
    return result

def bass_motion(wave, fps, start, duration):
    """Global-calibrated 30–160 Hz envelope plus low-frequency transient accents."""
    import numpy as np
    rate=22050;size=2048;window=np.hanning(size)
    bins=np.fft.rfftfreq(size,1/rate)
    mask=(bins>=30)&(bins<=160)
    midmask=(bins>=250)&(bins<=3500)
    highmask=(bins>=4000)&(bins<=10000)
    energies=[]; mids=[]; highs=[]
    for i in range(math.ceil(len(wave)/rate*fps)):
        at=max(0,round(i/fps*rate)-size//2)
        seg=wave[at:at+size]
        if len(seg)<size:seg=np.pad(seg,(0,size-len(seg)))
        fft=np.abs(np.fft.rfft(seg*window))
        energies.append(float(np.sqrt(np.mean(fft[mask]**2))))
        mids.append(float(np.sqrt(np.mean(fft[midmask]**2))))
        highs.append(float(np.sqrt(np.mean(fft[highmask]**2))))
    ref=max(1e-6,float(np.percentile(energies,96)))
    midref=max(1e-6,float(np.percentile(mids,96)))
    highref=max(1e-6,float(np.percentile(highs,96)))
    voice=0.; treble=0.
    envelope=0.;slow=0.;kick=0.;previous=0.;result=[]
    for index,energy in enumerate(energies):
        level=min(1.25,energy/ref)
        slow+=(1-math.exp(-1/(fps*.28)))*(level-slow)
        transient=max(0.,level-slow-.06)*2.8
        if level-previous>.045 and transient>.12:
            kick=max(kick,min(1.,transient))
        else:kick*=math.exp(-1/(fps*.13))
        envelope+=(.8 if level>envelope else 1-math.exp(-1/(fps*.15)))*(level-envelope)
        midlevel=min(1.,mids[index]/midref)
        highlevel=min(1.,highs[index]/highref)
        voice+=(.75 if midlevel>voice else .20)*(midlevel-voice)
        treble+=(.8 if highlevel>treble else .25)*(highlevel-treble)
        result.append((min(1.,envelope),kick,voice,treble))
        previous=level
    first=round(start*fps);count=math.ceil(duration*fps)
    return [result[min(first+i,len(result)-1)] for i in range(count)]


def ribbon(values,w,h):
    from PIL import Image,ImageDraw,ImageFilter
    import numpy as np
    base=Image.new("RGBA",(w,h),(0,0,0,0))
    glow=Image.new("RGBA",(w,h),(0,0,0,0));g=ImageDraw.Draw(glow)
    d=ImageDraw.Draw(base)
    half=np.interp(np.linspace(0,len(values)-1,28),np.arange(len(values)),values)
    values=np.concatenate((half[::-1],half))
    n=len(values);step=w/(n+2);bar=max(2,step*.48);cy=h/2
    for i,v in enumerate(values):
        x=(i+1.5)*step
        height=max(1.2,float(v)**1.25*h*.78)
        amber=max(0,1-abs(i-(n-1)/2)/(n*.20))*.65
        color=(round(184+amber*50),round(164+amber*30),round(244-amber*89))
        alpha=round(95+v*155)
        bounds=(x-bar/2,cy-height/2,x+bar/2,cy+height/2)
        g.rounded_rectangle((bounds[0]-2,bounds[1]-2,bounds[2]+2,bounds[3]+2),radius=bar,fill=(*color,round(alpha*.65)))
        d.rounded_rectangle(bounds,radius=bar/2,fill=(*color,alpha))
        if height>5:
            core=max(1,bar*.3)
            d.rounded_rectangle((x-core/2,cy-height*.42,x+core/2,cy+height*.42),radius=core/2,fill=(245,239,255,round(alpha*.9)))
    return Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(2,h*.055))),base)

def badge_geometry(w, h):
    portrait = h > w
    return w * (.465 if portrait else .5), h * (.42 if portrait else .49), min(w,h)*.26


def draw_badge(overlay, cfg, font):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
    w, h = overlay.size
    x, y, radius = badge_geometry(w, h)
    diameter = round(2*radius)
    glow = Image.new("RGBA", (w, h))
    ImageDraw.Draw(glow).ellipse((x-radius*1.10,y-radius*1.10,x+radius*1.10,y+radius*1.10),
                               fill=(174,28,48,32))
    overlay.alpha_composite(glow.filter(ImageFilter.GaussianBlur(radius*.19)))
    size = (diameter, diameter)
    badge = Image.new("RGBA", size, (8,11,14,255))
    if cfg.get("logo"):
        with Image.open(cfg["logo"]) as source:
            emblem = ImageOps.contain(source.convert("RGBA"), size, Image.Resampling.LANCZOS)
        overlay.alpha_composite(emblem, (round(x-emblem.width/2),round(y-emblem.height/2)))
        return
    else:
        draw = ImageDraw.Draw(badge)
        draw.ellipse((.42*diameter,.16*diameter,.58*diameter,.32*diameter), fill="#DFDAD0")
        wordmark = ImageFont.truetype(str(font), max(12,round(diameter*.105)))
        draw.text((radius, radius*1.13), cfg.get("brand","Nox FM"),
                  font=wordmark, fill="#F6F5EE", anchor="mm")
    mask = Image.new("L", size)
    ImageDraw.Draw(mask).ellipse((0,0,diameter-1,diameter-1), fill=255)
    badge.putalpha(mask)
    inset = diameter*.043
    ImageDraw.Draw(badge).ellipse((inset,inset,diameter-inset,diameter-inset),
                                outline="#F6F5EE", width=max(1,round(diameter*.009)))
    overlay.alpha_composite(badge, (round(x-radius),round(y-radius)))


from badge_effects import BadgeEffects


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project");ap.add_argument("--output");ap.add_argument("--ffmpeg")
    ap.add_argument("--check",action="store_true");ap.add_argument("--preview",type=float)
    ap.add_argument("--start",type=float,default=0.)
    args=ap.parse_args()
    ff=ffmpeg_path(args.ffmpeg)
    p,cfg,audio,wave,total,w,h,fps,scenes,cues=read_project(args.project,ff)
    if args.check:
        font_path(cfg.get("font"));font_path(cfg.get("font_bold"),True)
        print(json.dumps({"valid":True,"duration":total,"size":[w,h],"fps":fps,"scenes":len(scenes),"lyric_cues":len(cues)}));return
    start=args.start
    if not math.isfinite(start) or start<0 or start>=total:raise ValueError("Preview start is outside audio")
    if args.preview is not None and (not math.isfinite(args.preview) or args.preview<=0):raise ValueError("Preview duration must be positive")
    if args.preview is None and start:raise ValueError("--start is only for preview exports")
    duration=min(args.preview,total-start) if args.preview is not None else total
    filename=args.output or cfg.get("output","NoxFM_Music_Video.mp4")
    output=(p.parent/filename).resolve()
    if output.suffix.lower()!=".mp4":raise ValueError("Use an MP4 output")
    protected={audio,p}|{s["path"] for s in scenes}
    if cfg.get("logo"):
        protected.add(Path(cfg["logo"]))
    if output in protected:raise ValueError("Output would overwrite an input")
    output.parent.mkdir(parents=True,exist_ok=True)
    work=output.parent/(output.stem+"_work");work.mkdir(exist_ok=True)
    cfg['dynamic_logo'] = cfg.get('layout','badge') == 'badge'
    prepare_type(work,cfg,cues,w,h,start,duration)
    scenic=scenic_track(ff,work,scenes,w,h,fps,start,duration)
    values=analyze(wave,fps,start,duration)
    motion=bass_motion(wave,fps,start,duration)
    portrait=h>w
    vw=max(100,round(w*(.72 if portrait else .60)));vh=max(48,round(h*(.12 if portrait else .16)))
    vx=round(w*(.11 if portrait else .20));vy=round(h*(.49 if portrait else .53))
    badge = cfg.get("layout", "badge") == "badge"
    if badge:
        vw, vh = w, h
        effects = BadgeEffects(vw, vh, cfg.get('logo'))
        layers = f"[0:v][1:v]overlay=shortest=1[bg];[bg][3:v]overlay"
    else:
        layers = f"[0:v][3:v]overlay=0:0[bg];[bg][1:v]overlay={vx}:{vy}:shortest=1"
    vf = f"{layers},ass=captions.ass:fontsdir=fonts[v]"
    command=[ff,"-y","-v","error","-i",scenic.name,"-f","rawvideo","-pix_fmt","rgba","-s",f"{vw}x{vh}","-r",str(fps),"-i","pipe:0","-ss",str(start),"-i",str(audio),"-loop","1","-i","overlay.png","-filter_complex",vf,"-map","[v]","-map","2:a:0","-t",str(duration),"-c:v","libx264","-preset","veryfast","-crf",str(cfg.get("crf",20)),"-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-movflags","+faststart",str(output)]
    with (work/"encode.log").open("w",encoding="utf8") as log:
        proc=subprocess.Popen(command,cwd=work,stdin=subprocess.PIPE,stderr=log)
        try:
            for i,v in enumerate(values):
                frame = effects.frame(v, start+i/fps, *motion[i]) if badge else ribbon(v,vw,vh)
                proc.stdin.write(frame.tobytes())
                if i%max(1,fps*5)==0:print(json.dumps({"stage":"encode","progress":round(i/len(values)*100,1)}),flush=True)
            proc.stdin.close()
            if proc.wait():raise RuntimeError((work/"encode.log").read_text(encoding="utf8")[-6000:])
        except BaseException:
            proc.kill();proc.wait();raise
    # Actual frame preview and basic stream validation, without claiming audio is bit-identical.
    preview=output.with_suffix(".jpg")
    run([ff,"-y","-v","error","-ss",str(min(2,duration/2)),"-i",output,"-frames:v","1",preview])
    probe=subprocess.run([ff,"-hide_banner","-i",str(output)],capture_output=True,text=True)
    if "Video:" not in probe.stderr or "Audio:" not in probe.stderr:raise RuntimeError("Export is missing audio or video")
    shutil.copyfile(work/"captions.srt",output.with_suffix(".srt"))
    snapshot={**cfg,"rendered_output":str(output),"rendered_duration":duration,"preview_start":start,"source_project":str(p)}
    output.with_suffix(".project.json").write_text(json.dumps(snapshot,indent=2,ensure_ascii=False),encoding="utf8")
    print(json.dumps({"stage":"done","output":str(output),"duration":duration,"width":w,"height":h,"bytes":output.stat().st_size}),flush=True)

if __name__=="__main__":
    try:main()
    except (ValueError,RuntimeError,KeyError) as e:
        print(str(e),file=sys.stderr);sys.exit(1)

