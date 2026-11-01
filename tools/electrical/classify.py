import sys, json
def load(f):
    out=[]
    for l in open(f):
        x,y,w,h,n,c=l.split(); x,y,w,h=map(int,(x,y,w,h)); n=int(n[2:])
        r,g,b=int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)
        out.append(dict(x=x,y=y,w=w,h=h,n=n,r=r,g=g,b=b,cx=x+w/2,cy=y+h/2))
    return out
def mag(o): return o['r']>220 and 80<o['g']<120 and o['b']>230
def dblue(o): return o['b']>200 and o['r']<90 and o['g']<110
def inside(a,b,pad=2): return b['x']-pad<=a['x'] and b['y']-pad<=a['y'] and a['x']+a['w']<=b['x']+b['w']+pad and a['y']+a['h']<=b['y']+b['h']+pad
def classify(B):
    T={k:[] for k in "spot wall exhaust fan chand sb bedside fridge wagon ac down".split()}
    rings22=[o for o in B if mag(o) and 19<=o['w']<=25 and 19<=o['h']<=25]
    for o in B:
        w,h=o['w'],o['h']
        if mag(o) and 27<=w<=32 and 27<=h<=32: T['spot'].append(o)
        elif mag(o) and 19<=w<=25 and 19<=h<=25: T['wall'].append(o)
        elif mag(o) and 33<=w<=42 and 33<=h<=42 and not any(inside(r,o) for r in rings22): T['exhaust'].append(o)
        elif 0x90<=o['r']<=0xb8 and o['g']>0xa0 and o['b']<0x80 and 38<=w<=50 and 34<=h<=45: T['chand'].append(o)
        elif dblue(o) and ((20<=w<=24 and 13<=h<=18) or (13<=w<=18 and 20<=h<=24) or (17<=w<=21 and 13<=h<=15)) and o['n']>200: T['sb'].append(o)
        elif dblue(o) and 14<=w<=17 and 14<=h<=17: T['down'].append(o)
        elif dblue(o) and 36<=w<=48 and 36<=h<=48 and o['n']>250: T['bedside'].append(o)
        elif dblue(o) and 85<=w<=100 and 36<=h<=62 and o['n']>400:
            T['bedside'].append(dict(o,cx=o['x']+20,w=40)); T['bedside'].append(dict(o,cx=o['x']+w-20,w=40))
        elif o['r']>0xd0 and o['g']<0x70 and o['b']<0x60 and 36<=w<=48 and 36<=h<=48: T['fridge'].append(o)
        elif o['r']>0xe0 and o['g']>0xc8 and o['b']<0x90 and 40<=w<=52 and 40<=h<=52: T['wagon'].append(o)
        elif 0x90<=o['r']<=0xb8 and 0x70<=o['g']<=0x98 and o['b']>0xb8 and ((140<=w<=165 and 36<=h<=44) or (36<=w<=44 and 140<=h<=165)): T['ac'].append(o)
    # fans: cluster the blue dashes of the dashed circles
    dash=[o for o in B if dblue(o) and 20<=o['n']<=45 and max(o['w'],o['h'])<=17 and o not in T['sb']+T['down']]
    cl=[]
    for d in dash:
        for c in cl:
            if any(abs(d['cx']-e['cx'])<70 and abs(d['cy']-e['cy'])<70 for e in c): c.append(d); break
        else: cl.append([d])
    # merge clusters
    merged=True
    while merged:
        merged=False
        for i in range(len(cl)):
            for j in range(i+1,len(cl)):
                if any(abs(a['cx']-b['cx'])<70 and abs(a['cy']-b['cy'])<70 for a in cl[i] for b in cl[j]):
                    cl[i]+=cl.pop(j); merged=True; break
            if merged: break
    for c in cl:
        if len(c)>=10:
            xs=[d['cx'] for d in c]; ys=[d['cy'] for d in c]
            T['fan'].append(dict(cx=(min(xs)+max(xs))/2, cy=(min(ys)+max(ys))/2, w=max(xs)-min(xs)))
    return T
f, mp = sys.argv[1], sys.argv[2]
ox,sx,x0,oy,sy,y0 = map(float, mp.split(','))
T=classify(load(f))
res={}
for k,v in T.items():
    pts=[[round(ox+(o['cx']/2-x0)*sx), round(oy+(o['cy']/2-y0)*sy)] + ([1 if o['w']<o['h'] else 0] if k=='ac' else []) for o in v]
    res[k]=pts
    print(k, len(v), file=sys.stderr)
print(json.dumps(res, separators=(',',':')))
