#!/usr/bin/env python3
"""Prepare exact-lyric timing candidates, with explicit review flags."""
import argparse,json,math,os,re,shutil,subprocess,sys
from pathlib import Path

def tokenize(s):
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)?",s.lower().replace("’","'"),flags=re.UNICODE)
def normalize(s):return s.replace("'","")
def clean_lines(path):
    notes=re.compile(r"^\[(?:intro|verse|pre[- ]?chorus|post[- ]?chorus|chorus|bridge|outro|instrumental(?: break)?|end|final(?: line| chorus)?|brief silence|slow build|full[- ]band explosion|whispered|spoken)(?=\s*(?:\d+\b|[–—:\]\-]))",re.I)
    result=[]
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line=line.strip()
        if not line:continue
        if line.startswith("[") and line.endswith("]") and notes.search(line):continue
        result.append(line)
    if not result:raise ValueError("No sung lyrics were provided")
    return result

def transcribe(audio,cache,model_name,language,ffmpeg=None):
    import numpy as np
    os.environ.setdefault("HF_HOME",str(cache.resolve()))
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING","1")
    from faster_whisper import WhisperModel
    ff=ffmpeg or shutil.which("ffmpeg")
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    result=subprocess.run([str(ff),"-v","error","-i",str(audio),"-f","f32le","-ac","1","-ar","16000","pipe:1"],capture_output=True,check=True)
    wave=np.frombuffer(result.stdout,dtype=np.float32)
    model=WhisperModel(model_name,device="cpu",compute_type="int8",cpu_threads=min(4,os.cpu_count() or 2),download_root=str(cache))
    segments,_=model.transcribe(wave,language=language,beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
    words=[];rows=[]
    for s in segments:
        rows.append({"start":s.start,"end":s.end,"text":s.text})
        for w in s.words or []:
            words.append({"start":w.start,"end":w.end,"word":w.word,"probability":w.probability})
        print(json.dumps({"stage":"transcribe","seconds":round(s.end,2)}),flush=True)
    return {"words":words,"segments":rows}

def align(lines,transcript):
    expected=[];line_index=[]
    for i,line in enumerate(lines):
        for word in tokenize(line):
            expected.append(normalize(word));line_index.append(i)
    heard=[];times=[]
    for w in transcript["words"]:
        a,b=float(w["start"]),float(w["end"])
        if not math.isfinite(a+b) or a<0 or b<a:raise ValueError("Invalid transcript word timing")
        for token in tokenize(w["word"]):
            heard.append(normalize(token));times.append((a,b,float(w.get("probability",1))))
    if not heard:raise ValueError("Transcription produced no words; use another model or manual timing")
    n,m=len(expected),len(heard)
    if n*m>12000000:raise ValueError("Align this long recording in separate song sections")
    # Global sequence matching handles ordinary transcription substitutions.
    # It is not forced alignment and deliberately does not invent missing times.
    trace=[bytearray(m+1) for _ in range(n+1)]
    prev=[j*.75 for j in range(m+1)]
    for j in range(1,m+1):trace[0][j]=2
    for i in range(1,n+1):
        curr=[i*.75]+[0.]*m;trace[i][0]=1
        for j in range(1,m+1):
            costs=(prev[j-1]+(0 if expected[i-1]==heard[j-1] else 1.05),prev[j]+.75,curr[j-1]+.75)
            k=min(range(3),key=costs.__getitem__);curr[j]=costs[k];trace[i][j]=k
        prev=curr
    pairs=[];i,j=n,m
    while i or j:
        k=trace[i][j]
        if k==0:
            if expected[i-1]==heard[j-1]:pairs.append((i-1,j-1))
            i-=1;j-=1
        elif k==1:i-=1
        else:j-=1
    pairs.reverse();grouped=[[] for _ in lines]
    for a,b in pairs:grouped[line_index[a]].append(b)
    cues=[];issues=[]
    for i,line in enumerate(lines):
        matched=grouped[i];count=len(tokenize(line));ratio=len(matched)/max(1,count)
        a=times[matched[0]][0] if matched else None
        b=times[matched[-1]][1] if matched else None
        reasons=[]
        if not matched:reasons.append("No matched vocal words; supply actual timing")
        if ratio<.7:reasons.append("Low lyric-word coverage")
        if matched and sum(times[k][2] for k in matched)/len(matched)<.6:reasons.append("Low transcription confidence")
        if a is not None and (b-a>max(8,count*.85) or b<=a):reasons.append("Check long sustain, pause or unreliable timing")
        cue={"start":a,"end":b,"text":line,"chorus":line.isupper(),"coverage":round(ratio,3),"needs_review":bool(reasons)}
        cues.append(cue)
        if reasons:issues.append({"cue":i,"text":line,"reasons":reasons})
    for i in range(1,len(cues)):
        before,current=cues[i-1],cues[i]
        if before["end"] is not None and current["start"] is not None and current["start"]<before["end"]-.01:
            current["needs_review"]=True
            issues.append({"cue":i,"text":current["text"],"reasons":["Overlapping candidates; review actual vocal transition"]})
    return cues,issues

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audio",type=Path);p.add_argument("--lyrics",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--transcript",type=Path)
    p.add_argument("--cache",type=Path,default=Path(".unkownsongs-models"))
    p.add_argument("--model",default="small.en");p.add_argument("--language",default="en");p.add_argument("--ffmpeg")
    args=p.parse_args()
    lines=clean_lines(args.lyrics)
    args.out=args.out.resolve();args.out.parent.mkdir(parents=True,exist_ok=True)
    if args.transcript:
        t=json.loads(args.transcript.read_text(encoding="utf-8-sig"))
    else:
        if not args.audio or not args.audio.is_file():raise ValueError("Provide --audio or an existing --transcript")
        args.cache.mkdir(parents=True,exist_ok=True)
        t=transcribe(args.audio.resolve(),args.cache.resolve(),args.model,args.language,args.ffmpeg)
        args.out.with_suffix(".transcript.json").write_text(json.dumps(t,indent=2,ensure_ascii=False),encoding="utf8")
    cues,issues=align(lines,t)
    args.out.write_text(json.dumps(cues,indent=2,ensure_ascii=False),encoding="utf8")
    report={"cue_count":len(cues),"requires_review":len({i["cue"] for i in issues}),"issues":issues,
            "note":"Candidate sequence matching, not verified forced alignment. Review repeats, ad-libs and musical gaps."}
    args.out.with_suffix(".report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
    print(json.dumps({"output":str(args.out),"cue_count":len(cues),"requires_review":report["requires_review"]}),flush=True)

if __name__=="__main__":
    try:main()
    except (ValueError,KeyError,RuntimeError,subprocess.CalledProcessError) as e:
        print(str(e),file=sys.stderr);sys.exit(1)
