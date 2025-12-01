# init pygame
import pygame
import random
import math
import heapq

# init pygame
pygame.init()
# set window
W, H = 1000, 750
# create surface
s = pygame.display.set_mode((W, H))
# set title
pygame.display.set_caption("Space Graph Thing")
# create clock
c = pygame.time.Clock()

# color black
BK = (0, 0, 0)
# color white
WH = (255, 255, 255)
# color yellow
YL = (255, 255, 100)
# color blue
BL = (80, 100, 220)
# color grey
GR = (120, 120, 120)
# palette colors
PC = [(255, 150, 50), (70, 220, 180), (200, 80, 255)]


# black hole
class BH:
    def __init__(self, x, y):
        # set pos
        self.x = x
        self.y = y
        # radius small
        self.r = 30

    def draw(self, scr):
        # draw halo
        pygame.draw.circle(scr, (20, 20, 40), (int(self.x), int(self.y)), 130)
        # draw inner
        pygame.draw.circle(scr, (10, 10, 20), (int(self.x), int(self.y)), 100)
        # draw core
        pygame.draw.circle(scr, BK, (int(self.x), int(self.y)), self.r)


# planet class
class P:
    def __init__(self, ph, od, sa):
        # parent hole
        self.ph = ph
        # orbit distance
        self.od = od
        # angle start
        self.a = sa
        # speed random
        self.sp = random.uniform(0.0015, 0.003)
        # position x
        self.x = 0.0
        # position y
        self.y = 0.0
        # size base
        self.sz = 15
        # update pos
        self.upd()

    def upd(self):
        # advance angle
        self.a += self.sp
        # normalize angle
        self.a %= 2 * math.pi
        # compute x
        self.x = self.ph.x + self.od * math.cos(self.a)
        # compute y
        self.y = self.ph.y + self.od * math.sin(self.a)

    def draw(self, scr):
        # draw glow
        pygame.draw.circle(
            scr, (255, 255, 150), (int(self.x), int(self.y)), self.sz + 3
        )
        # draw core
        pygame.draw.circle(scr, YL, (int(self.x), int(self.y)), self.sz)

    def d(self, x, y):
        # distance calc
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


# satellite class
class S:
    def __init__(self, o):
        # owner planet
        self.o = o
        # orbit distance
        self.od = random.randint(35, 65)
        # angle init
        self.a = random.uniform(
            0, 2 * math.pi
        )  # Random initial angle for orbital motion
        # rotation speed
        self.rs = random.uniform(0.015, 0.025)
        # pos x
        self.x = 0.0
        # pos y
        self.y = 0.0
        # history points
        self.h = []
        # history max
        self.hm = 12
        # update pos
        self.upd()

    def upd(self):
        # radius factor
        r = 0.8 + (40.0 / self.od)
        # advance angle
        self.a += self.rs * r
        # compute x
        self.x = self.o.x + self.od * math.cos(self.a)
        # compute y
        self.y = self.o.y + self.od * math.sin(self.a)
        # append history
        self.h.append((self.x, self.y))
        # trim history
        if len(self.h) > self.hm:
            self.h.pop(0)

    def draw(self, scr):
        # draw trail
        p = self.h
        for i in range(1, len(p)):
            pygame.draw.line(scr, (200, 200, 200), p[i - 1], p[i], 2)
        # draw dot
        pygame.draw.circle(scr, WH, (int(self.x), int(self.y)), 4)

    def d(self, x, y):
        # distance calc
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


# stray star
class St:
    def __init__(self):
        # random x
        self.x = random.randint(0, W)
        # random y
        self.y = random.randint(0, H)
        # size pick
        self.sz = random.choice([1, 2, 2])
        # speed value
        self.sp = random.uniform(0.08, 0.25)
        # captured body
        self.cb = None
        # capture angle
        self.ca = 0
        # capture dist
        self.cd = 0

    def upd(self, pl):
        # if free
        if self.cb is None:
            # find close
            cls = None
            cd = float("inf")
            for p in pl:
                d = self.d(p.x, p.y)
                if d < cd:
                    cd = d
                    cls = p
            # approach target
            if cls:
                dx = cls.x - self.x
                dy = cls.y - self.y
                dt = math.sqrt(dx * dx + dy * dy)
                if dt > 0.1:
                    self.x += (dx / dt) * self.sp
                    self.y += (dy / dt) * self.sp
                # capture check
                if self.d(cls.x, cls.y) < cls.sz + 25:
                    self.cb = cls
                    self.cd = self.d(cls.x, cls.y)
                    self.ca = math.atan2(self.y - cls.y, self.x - cls.x)
        else:
            # orbit capture
            self.ca += 0.02
            self.x = self.cb.x + self.cd * math.cos(self.ca)
            self.y = self.cb.y + self.cd * math.sin(self.ca)

    def draw(self, scr):
        # draw star
        pygame.draw.circle(scr, WH, (int(self.x), int(self.y)), self.sz)

    def d(self, x, y):
        # distance calc
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


# dijkstra algorithm
def dij(am, st, nn):
    ds = [float("inf")] * nn
    pr = [-1] * nn
    # start distance
    ds[st] = 0
    # heap queue
    hq = [(0, st)]
    while hq:
        cd, u = heapq.heappop(hq)
        # stale entry
        if cd > ds[u]:
            continue
        for v in range(nn):
            if am[u][v] < float("inf"):
                nd = ds[u] + am[u][v]
                if nd < ds[v]:
                    ds[v] = nd
                    pr[v] = u
                    heapq.heappush(hq, (nd, v))
    return ds, pr


# get path
def gp(pr, st, ed):
    pth = []
    cr = ed
    # backtrack path
    while cr != -1:
        pth.append(cr)
        cr = pr[cr]
    pth.reverse()
    return pth if pth and pth[0] == st else []


# build graph
def bg(pl, st, bh):
    # aggregate nodes
    an = pl + st + [bh]
    n = len(an)
    # adjacency matrix
    am = [[float("inf")] * n for _ in range(n)]
    # planet links
    for i in range(len(pl)):
        for j in range(i + 1, len(pl)):
            dx = pl[i].x - pl[j].x
            dy = pl[i].y - pl[j].y
            d = math.sqrt(dx * dx + dy * dy)
            if d < 350:
                am[i][j] = d
                am[j][i] = d
    # satellite links
    for si, sat in enumerate(st):
        ni = len(pl) + si
        pi = pl.index(sat.o)
        d = sat.od
        am[ni][pi] = d
        am[pi][ni] = d
    # blackhole links
    bi = len(an) - 1
    for i, pt in enumerate(pl):
        dx = pt.x - bh.x
        dy = pt.y - bh.y
        d = math.sqrt(dx * dx + dy * dy)
        if d < 450:
            am[i][bi] = d
            am[bi][i] = d
    return am, an


# draw path
def dp(scr, nl, col):
    if len(nl) < 2:
        return
    for idx in range(len(nl) - 1):
        n1 = nl[idx]
        n2 = nl[idx + 1]
        # endpoints pos
        x1, y1 = n1.x, n1.y
        x2, y2 = n2.x, n2.y
        # midpoint compute
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        dx = x2 - x1
        dy = y2 - y1
        ln = math.sqrt(dx * dx + dy * dy)
        if ln > 0:
            # perpendicular dir
            px = -dy / ln
            py = dx / ln
            cv = 0.3 + (ln / 800.0) * 0.2
            cx = mx + px * ln * cv
            cy = my + py * ln * cv
        else:
            cx, cy = mx, my
        # bezier start
        lx, ly = x1, y1
        ns = 20
        for st in range(1, ns + 1):
            t = st / float(ns)
            mt = 1.0 - t
            px = mt * mt * x1 + 2 * mt * t * cx + t * t * x2
            py = mt * mt * y1 + 2 * mt * t * cy + t * t * y2
            pygame.draw.line(scr, col, (int(lx), int(ly)), (int(px), int(py)), 4)
            lx, ly = px, py


# create blackhole
bh = BH(W / 2, H / 2)
# create planets
pl = []
for _ in range(5):
    d = random.randint(130, 280)
    a = random.uniform(0, 2 * math.pi)
    pl.append(P(bh, d, a))

# create satellites
st = []
for _ in range(12):
    st.append(S(random.choice(pl)))

# create strays
strs = [St() for _ in range(40)]
# shortest path list
spth = []
# click selection
csl = []
# color index
cco = 0

# main loop
run = True
while run:
    # clear screen
    s.fill((8, 8, 20))
    for ev in pygame.event.get():
        # quit event
        if ev.type == pygame.QUIT:
            run = False
        # mouse click
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos
            cl = None
            # check planets
            for ix, p in enumerate(pl):
                if p.d(mx, my) < p.sz + 8:
                    cl = ix
                    break
            # check satellites
            if cl is None:
                for ix, sat in enumerate(st):
                    if sat.d(mx, my) < 8:
                        cl = len(pl) + ix
                        break
            # check blackhole
            if cl is None:
                if math.sqrt((mx - bh.x) ** 2 + (my - bh.y) ** 2) < bh.r + 10:
                    cl = len(pl) + len(st)
            # record selection
            if cl is not None:
                csl.append(cl)
                if len(csl) == 2:
                    am, an = bg(pl, st, bh)
                    ds, pr = dij(am, csl[0], len(an))
                    if pr[csl[1]] != -1:
                        pi = gp(pr, csl[0], csl[1])
                        if pi:
                            pn = [an[i] for i in pi]
                            col = PC[cco % len(PC)]
                            cco += 1
                            spth.append((pn, col))
                    csl = []

    # update planets
    for p in pl:
        p.upd()
    # update satellites
    for sat in st:
        sat.upd()
    # update strays
    for str in strs:
        str.upd(pl)

    # draw blackhole
    bh.draw(s)
    # build graph
    am, an = bg(pl, st, bh)
    # draw edges
    for i in range(len(an)):
        for j in range(i + 1, len(an)):
            if am[i][j] < float("inf"):
                n1 = an[i]
                n2 = an[j]
                pygame.draw.line(
                    s, (60, 80, 220), (int(n1.x), int(n1.y)), (int(n2.x), int(n2.y)), 1
                )

    # draw shortest paths
    for pn, col in spth:
        dp(s, pn, col)

    # draw satellites
    for sat in st:
        sat.draw(s)
    # draw planets
    for p in pl:
        p.draw(s)
    # draw strays
    for str in strs:
        str.draw(s)

    # info text
    f = pygame.font.SysFont(None, 32)
    t = f.render("Click two objects to find shortest path", True, (200, 200, 255))
    s.blit(t, (20, 20))
    if csl:
        slt = f.render(f"Selected: {len(csl)}/2", True, (255, 200, 100))
        s.blit(slt, (20, 60))

    # flip display
    pygame.display.flip()
    # cap framerate
    c.tick(60)

# quit pygame
pygame.quit()
