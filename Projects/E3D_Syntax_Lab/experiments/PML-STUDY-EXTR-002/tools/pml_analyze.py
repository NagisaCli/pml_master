import re, math, sys, json

SRC = sys.argv[1]
lines = open(SRC, encoding='utf-8', errors='replace').read().splitlines()

dirs = {'E':(1,0,0),'W':(-1,0,0),'N':(0,1,0),'S':(0,-1,0),'U':(0,0,1),'D':(0,0,-1)}
attr_re = re.compile(r'^\s*([A-Z][A-Z0-9_]*)\s+(.+?)\s*$')

def parse_ori(s):
    axes = {}
    for part in s.upper().split('AND'):
        part = part.strip()
        m = re.match(r'([XYZ])\s+IS\s+([EWNSUD])(?:\s+(\d+(?:\.\d+)?)\s+([EWNSUD]))?', part)
        if not m:
            return None
        if m.group(3):
            ang = math.radians(float(m.group(3)))
            v1, v2 = dirs[m.group(2)], dirs[m.group(4)]
            axes[m.group(1)] = tuple(v1[i]*math.cos(ang)+v2[i]*math.sin(ang) for i in range(3))
        else:
            axes[m.group(1)] = dirs[m.group(2)]
    return axes

def num(s):
    m = re.search(r'(-?\d+(?:\.\d+)?)', s.replace(',', ''))
    return float(m.group(1)) if m else 0.0

def vec_attr(s):
    mm = re.findall(r'([EWNSUD])\s*(-?\d+(?:\.\d+)?)mm', s or '')
    out = {'E':0.,'W':0.,'N':0.,'S':0.,'U':0.,'D':0.}
    for d, v in mm:
        out[d] = float(v)
    return [out['E']-out['W'], out['N']-out['S'], out['U']-out['D']]

def attrd(e, name):
    for k, v in e['attrs']:
        if k == name:
            return v
    return None

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def bbox_of(e):
    t = e['type']
    try:
        pos_s = attrd(e,'POS'); pos = vec_attr(pos_s) if pos_s else [0,0,0]
        ori = parse_ori(attrd(e,'ORI') or 'Y IS N AND Z IS U')
        if ori is None:
            yv, zv = (0,1,0), (0,0,1)
        else:
            yv, zv = ori['Y'], ori['Z']
        xv = cross(yv, zv)
        def g(p):
            return (pos[0]+p[0]*xv[0]+p[1]*yv[0]+p[2]*zv[0],
                    pos[1]+p[0]*xv[1]+p[1]*yv[1]+p[2]*zv[1],
                    pos[2]+p[0]*xv[2]+p[1]*yv[2]+p[2]*zv[2])
        if t == 'EXTRUSION':
            h = num(attrd(e,'HEIG') or '0')
            pts = []
            for vs in e['verts']:
                v = vec_attr(vs)
                pts.append(g((v[0], v[1], 0)))
                pts.append(g((v[0], v[1], h)))
            return pts
        if t == 'CYLINDER':
            d = num(attrd(e,'DIAM') or '0')/2; h = num(attrd(e,'HEIG') or '0')
            pts = []
            for sx in (-1,1):
                for sy in (-1,1):
                    for sz in (0,1):
                        pts.append(g((sx*d, sy*d, sz*h)))
            return pts
        if t == 'BOX':
            xl = num(attrd(e,'XLEN') or '0')/2; yl = num(attrd(e,'YLEN') or '0')/2; zl = num(attrd(e,'ZLEN') or '0')/2
            pts = []
            for sx in (-1,1):
                for sy in (-1,1):
                    for sz in (-1,1):
                        pts.append(g((sx*xl, sy*yl, sz*zl)))
            return pts
        if t == 'PYRAMID':
            xb = num(attrd(e,'XBOT') or '0')/2; yb = num(attrd(e,'YBOT') or '0')/2
            xt = num(attrd(e,'XTOP') or '0')/2; yt = num(attrd(e,'YTOP') or '0')/2
            h = num(attrd(e,'HEIG') or '0'); xo = num(attrd(e,'XOFF') or '0'); yo = num(attrd(e,'YOFF') or '0')
            pts = []
            for sx,sy,sz in ((1,1,0),(1,-1,0),(-1,-1,0),(-1,1,0),(1,1,1),(1,-1,1),(-1,-1,1),(-1,1,1)):
                dx = xb if sz == 0 else xt; dy = yb if sz == 0 else yt
                pts.append(g((sx*dx+xo, sy*dy+yo, sz*h)))
            return pts
    except Exception:
        pass
    return None

stack = []
elems = []
for lineno, raw in enumerate(lines, 1):
    line = raw.strip()
    if not line:
        continue
    if line.upper().startswith('NEW '):
        m = re.match(r'NEW\s+(\S+)\s*(.*)', line, re.I)
        typ = m.group(1).upper(); rest = m.group(2).strip()
        rec = {'type':typ, 'rest':rest, 'attrs':[], 'verts':[], 'children':[], 'line':lineno, 'rawline':line}
        if stack:
            stack[-1]['children'].append(rec); rec['parent'] = stack[-1]
        else:
            rec['parent'] = None
        stack.append(rec)
        if typ in ('EQUIPMENT','SUBEQUIPMENT'):
            nm = re.search(r'/([A-Za-z0-9_.\-]+)', rest); rec['name'] = nm.group(1) if nm else ''
        elif typ in ('EXTRUSION','CYLINDER','BOX','DISH','PYRAMID','CONE','TORUS','SPHERE'):
            elems.append(rec)
        continue
    if line.upper() == 'END':
        if stack:
            stack.pop()
        continue
    if not stack:
        continue
    cur = stack[-1]
    if cur['type'] == 'VERTEX':
        mm = re.match(r'POS\s+(.+)$', line, re.I)
        if mm:
            cur['attrs'].append(('POS', mm.group(1)))
    else:
        mm = attr_re.match(line)
        if mm:
            cur['attrs'].append((mm.group(1).upper(), mm.group(2)))

for e in elems:
    if e['type'] == 'EXTRUSION':
        verts = []
        def walk(n):
            for c in n.get('children', []):
                if c['type'] == 'VERTEX':
                    pos = ''
                    for k, v in c['attrs']:
                        if k == 'POS':
                            pos = v
                    verts.append(pos)
                else:
                    walk(c)
        walk(e)
        e['verts'] = verts
    p = e['parent']; sub = 'GLOBAL'
    while p:
        if p['type'] in ('SUBEQUIPMENT','EQUIPMENT'):
            sub = p.get('name', p['type'])
            break
        p = p['parent']
    e['sub'] = sub
    e['bb'] = bbox_of(e)

def circle_fit(pts2d):
    n = len(pts2d)
    if n < 3:
        return None
    xs = [p[0] for p in pts2d]; ys = [p[1] for p in pts2d]
    xm = sum(xs)/n; ym = sum(ys)/n
    ux = [x-xm for x in xs]; uy = [y-ym for y in ys]
    su = sum(x*x+y*y for x,y in zip(ux,uy))
    A = [[sum(2*x*x for x in ux), sum(2*x*y for x,y in zip(ux,uy))],
         [sum(2*x*y for x,y in zip(ux,uy)), sum(2*y*y for y in uy)]]
    b = [sum(x*(x*x+y*y) for x,y in zip(ux,uy)), sum(y*(x*x+y*y) for x,y in zip(ux,uy))]
    det = A[0][0]*A[1][1]-A[0][1]*A[1][0]
    if abs(det) < 1e-12:
        return None
    cx = (b[0]*A[1][1]-b[1]*A[0][1])/det
    cy = (A[0][0]*b[1]-A[0][1]*b[0])/det
    r = math.sqrt(cx*cx+cy*cy+su/n)
    cx += xm; cy += ym
    devs = [abs(math.hypot(x-cx, y-cy)-r) for x,y in pts2d]
    return (cx, cy, r, max(devs))

if __name__ == '__main__':
    mode = sys.argv[2] if len(sys.argv) > 2 else 'summary'
    if mode == 'summary':
        from collections import Counter
        subs = {}
        for e in elems:
            subs.setdefault(e['sub'], []).append(e)
        print('total geometry:', len(elems))
        for sub, el in sorted(subs.items()):
            c = Counter(x['type'] for x in el)
            print(f"{sub}: {len(el)} -> {dict(c)}")
            for typ in ('EXTRUSION','CYLINDER','BOX'):
                ex = [x for x in el if x['type'] == typ]
                if not ex:
                    continue
                vc = Counter(len(x['verts']) for x in ex if x['type']=='EXTRUSION')
                if vc:
                    print('   EXTRUSION vertex-counts:', dict(sorted(vc.items())))
                pts = [p for x in ex if x['bb'] for p in x['bb']]
                if pts:
                    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; zs=[p[2] for p in pts]
                    print(f"   {typ} bbox: X[{min(xs):.1f},{max(xs):.1f}] Y[{min(ys):.1f},{max(ys):.1f}] Z[{min(zs):.1f},{max(zs):.1f}]")
    elif mode == 'detail':
        subfilter = sys.argv[3] if len(sys.argv) > 3 else ''
        for e in elems:
            if subfilter and e['sub'] != subfilter:
                continue
            bb = e['bb']
            siz = ''
            if e['type'] == 'EXTRUSION':
                siz = f"nv={len(e['verts']):3d} h={num(attrd(e,'HEIG') or '0'):7.1f}"
            elif e['type'] == 'CYLINDER':
                siz = f"d={num(attrd(e,'DIAM') or '0'):7.1f} h={num(attrd(e,'HEIG') or '0'):7.1f}"
            elif e['type'] == 'BOX':
                siz = f"xl={num(attrd(e,'XLEN') or '0'):7.1f} yl={num(attrd(e,'YLEN') or '0'):7.1f} zl={num(attrd(e,'ZLEN') or '0'):7.1f}"
            else:
                siz = ''
            if bb:
                xs=[p[0] for p in bb]; ys=[p[1] for p in bb]; zs=[p[2] for p in bb]
                print(f"{e['sub']:26s} line {e['line']:6d} {e['type']:9s} {siz} X[{min(xs):8.1f},{max(xs):8.1f}] Y[{min(ys):8.1f},{max(ys):8.1f}] Z[{min(zs):7.1f},{max(zs):7.1f}] POS={attrd(e,'POS')} ORI={attrd(e,'ORI')}")
            else:
                print(f"{e['sub']:26s} line {e['line']:6d} {e['type']:9s} {siz} POS={attrd(e,'POS')} ORI={attrd(e,'ORI')}")
    elif mode == 'sig':
        for e in elems:
            sig = e['type']
            for k in ('POS','ORI','HEIG','DIAM','XLEN','YLEN','ZLEN'):
                v = attrd(e,k)
                if v:
                    sig += '|' + k + '=' + v.replace(' ', '')
            if e['type'] == 'EXTRUSION':
                sig += '|nv=' + str(len(e['verts']))
                if len(e['verts']) <= 12:
                    sig += '|' + ';'.join(e['verts']).replace(' ', '')
            print(f"{e['sub']}\t{e['line']}\t{sig}")
