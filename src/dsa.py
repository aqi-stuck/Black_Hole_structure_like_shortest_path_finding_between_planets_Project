import pygame
import random
import math
import heapq

pygame.init()
W, H = 1000, 750
s = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Graph Thing")
c = pygame.time.Clock()

# Color definitions
BK = (0, 0, 0)
WH = (255, 255, 255)
YL = (255, 255, 100)
BL = (80, 100, 220)
GR = (120, 120, 120)
PC = [(255, 150, 50), (70, 220, 180), (200, 80, 255)]


# Black hole at the center of the system
class BH:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 30  # Collision radius

    def draw(self, scr):
        # Draw concentric circles to represent a black hole
        pygame.draw.circle(scr, (20, 20, 40), (int(self.x), int(self.y)), 130)
        pygame.draw.circle(scr, (10, 10, 20), (int(self.x), int(self.y)), 100)
        pygame.draw.circle(scr, BK, (int(self.x), int(self.y)), self.r)


# Planet class: orbits around a black hole
class P:
    def __init__(self, ph, od, sa):
        self.ph = ph  # Parent black hole
        self.od = od  # Orbital distance
        self.a = sa   # Current angle
        self.sp = random.uniform(0.0015, 0.003)  # Angular speed
        self.x = 0.0
        self.y = 0.0
        self.sz = 15  # Size for collision detection

    def upd(self):
        # Update position based on circular orbit
        self.a += self.sp
        self.a %= 2 * math.pi
        self.x = self.ph.x + self.od * math.cos(self.a)
        self.y = self.ph.y + self.od * math.sin(self.a)

    def draw(self, scr):
        # Draw planet as a yellow circle
        pygame.draw.circle(
            scr, (255, 255, 150), (int(self.x), int(self.y)), self.sz + 3
        )
        pygame.draw.circle(scr, YL, (int(self.x), int(self.y)), self.sz)

    def d(self, x, y):
        # Calculate distance to a point
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


# Satellite class: orbits around planets
class S:
    def __init__(self, o):
        self.o = o  # Parent orbit (planet)
        self.od = random.randint(35, 65)  # Orbital distance
        self.a = random.uniform(0, 2 * math.pi)  # Current angle
        self.rs = random.uniform(0.015, 0.025)  # Rotation speed
        self.x = 0.0
        self.y = 0.0
        self.h = []  # History of positions (for trail)
        self.hm = 12  # Max history points

    def upd(self):
        # Update position based on orbit around planet
        r = 0.8 + (40.0 / self.od)  # Speed modifier based on distance
        self.a += self.rs * r
        self.x = self.o.x + self.od * math.cos(self.a)
        self.y = self.o.y + self.od * math.sin(self.a)
        self.h.append((self.x, self.y))
        if len(self.h) > self.hm:
            self.h.pop(0)  # Remove old trail points

    def draw(self, scr):
        # Draw orbit trail and satellite
        p = self.h
        for i in range(1, len(p)):
            pygame.draw.line(scr, (200, 200, 200), p[i - 1], p[i], 2)
        pygame.draw.circle(scr, WH, (int(self.x), int(self.y)), 4)

    def d(self, x, y):
        # Calculate distance to a point
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


# Star/meteoroid class: free-moving objects attracted to planets
class St:
    def __init__(self):
        self.x = random.randint(0, W)
        self.y = random.randint(0, H)
        self.sz = random.choice([1, 2, 2])  # Size
        self.sp = random.uniform(0.08, 0.25)  # Movement speed
        self.cb = None  # Currently bound to (orbiting) a planet
        self.ca = 0  # Current orbit angle
        self.cd = 0  # Current orbit distance

    def upd(self, pl):
        # Update position: move toward nearest planet or orbit if bound
        if self.cb is None:
            # Find nearest planet
            cls = None
            cd = float("inf")
            for p in pl:
                d = self.d(p.x, p.y)
                if d < cd:
                    cd = d
                    cls = p
            if cls:
                # Move toward nearest planet
                dx = cls.x - self.x
                dy = cls.y - self.y
                dt = math.sqrt(dx * dx + dy * dy)
                if dt > 0.1:
                    self.x += (dx / dt) * self.sp
                    self.y += (dy / dt) * self.sp
                # Bind to planet when close enough
                if self.d(cls.x, cls.y) < cls.sz + 25:
                    self.cb = cls
                    self.cd = self.d(cls.x, cls.y)
                    self.ca = math.atan2(self.y - cls.y, self.x - cls.x)
        else:
            # Orbit around bound planet
            self.ca += 0.02
            self.x = self.cb.x + self.cd * math.cos(self.ca)
            self.y = self.cb.y + self.cd * math.sin(self.ca)

    def draw(self, scr):
        # Draw star as white circle
        pygame.draw.circle(scr, WH, (int(self.x), int(self.y)), self.sz)

    def d(self, x, y):
        # Calculate distance to a point
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


# Dijkstra's shortest path algorithm
def dij(am, st, nn):
    """
    Find shortest paths from start node to all others.
    am: adjacency matrix with distances
    st: start node index
    nn: number of nodes
    Returns: (distances, predecessors)
    """
    ds = [float("inf")] * nn  # Distance to each node
    pr = [-1] * nn  # Predecessor for path reconstruction
    ds[st] = 0
    hq = [(0, st)]  # Min-heap: (distance, node)
    
    while hq:
        cd, u = heapq.heappop(hq)
        if cd > ds[u]:
            continue  # Skip if we've found a better path
        # Explore neighbors
        for v in range(nn):
            if am[u][v] < float("inf"):
                nd = ds[u] + am[u][v]
                if nd < ds[v]:
                    ds[v] = nd
                    pr[v] = u
                    heapq.heappush(hq, (nd, v))
    
    return ds, pr


# Reconstruct path from Dijkstra result
def gp(pr, st, ed):
    """
    Get path from start to end using predecessor array.
    Returns list of node indices representing the path.
    """
    pth = []
    cr = ed
    while cr != -1:
        pth.append(cr)
        cr = pr[cr]
    pth.reverse()
    return pth if pth and pth[0] == st else []


# Build graph from space objects
def bg(pl, st, bh):
    """
    Build adjacency matrix and node list from planets, satellites, and black hole.
    Connects nearby objects with edges representing traversable distances.
    """
    an = pl + st + [bh]  # All nodes: planets + satellites + black hole
    n = len(an)
    am = [[float("inf")] * n for _ in range(n)]  # Adjacency matrix
    
    # Connect planets within 350 pixels
    for i in range(len(pl)):
        for j in range(i + 1, len(pl)):
            dx = pl[i].x - pl[j].x
            dy = pl[i].y - pl[j].y
            d = math.sqrt(dx * dx + dy * dy)
            if d < 350:
                am[i][j] = d
                am[j][i] = d
    
    # Connect satellites to their parent planets
    for si, sat in enumerate(st):
        ni = len(pl) + si
        pi = pl.index(sat.o)
        d = sat.od
        am[ni][pi] = d
        am[pi][ni] = d
    
    # Connect black hole to nearby planets
    bi = len(an) - 1
    for i, pt in enumerate(pl):
        dx = pt.x - bh.x
        dy = pt.y - bh.y
        d = math.sqrt(dx * dx + dy * dy)
        if d < 450:
            am[i][bi] = d
            am[bi][i] = d
    
    return am, an


# Draw path with curved lines
def dp(scr, nl, col):
    """
    Draw a path as a series of curved lines using quadratic Bezier curves.
    nl: list of nodes to connect
    col: color of the path
    """
    if len(nl) < 2:
        return
    for idx in range(len(nl) - 1):
        n1 = nl[idx]
        n2 = nl[idx + 1]
        x1, y1 = n1.x, n1.y
        x2, y2 = n2.x, n2.y
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        dx = x2 - x1
        dy = y2 - y1
        ln = math.sqrt(dx * dx + dy * dy)
        
        # Calculate control point for curve
        if ln > 0:
            px = -dy / ln
            py = dx / ln
            cv = 0.3 + (ln / 800.0) * 0.2
            cx = mx + px * ln * cv
            cy = my + py * ln * cv
        else:
            cx, cy = mx, my
        
        # Draw Bezier curve with line segments
        lx, ly = x1, y1
        ns = 20  # Number of segments
        for st in range(1, ns + 1):
            t = st / float(ns)
            mt = 1.0 - t
            # Quadratic Bezier formula
            px = mt * mt * x1 + 2 * mt * t * cx + t * t * x2
            py = mt * mt * y1 + 2 * mt * t * cy + t * t * y2
            pygame.draw.line(scr, col, (int(lx), int(ly)), (int(px), int(py)), 4)
            lx, ly = px, py


# Initialize space system
bh = BH(W / 2, H / 2)
pl = []  # Planets
for _ in range(5):
    d = random.randint(130, 280)
    a = random.uniform(0, 2 * math.pi)
    pl.append(P(bh, d, a))

st = []  # Satellites
for _ in range(12):
    st.append(S(random.choice(pl)))

strs = [St() for _ in range(40)]  # Stars/meteoroids
spth = []  # Shortest paths found
csl = []  # Currently selected nodes
cco = 0   # Color counter

# Main game loop
run = True
while run:
    s.fill((8, 8, 20))
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
        
        # Handle clicks to select nodes and find paths
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos
            cl = None
            
            # Check if planet clicked
            for ix, p in enumerate(pl):
                if p.d(mx, my) < p.sz + 8:
                    cl = ix
                    break
            
            # Check if satellite clicked
            if cl is None:
                for ix, sat in enumerate(st):
                    if sat.d(mx, my) < 8:
                        cl = len(pl) + ix
                        break
            
            # Check if black hole clicked
            if cl is None:
                if math.sqrt((mx - bh.x) ** 2 + (my - bh.y) ** 2) < bh.r + 10:
                    cl = len(pl) + len(st)
            
            # Add to selection and compute path if two nodes selected
            if cl is not None:
                csl.append(cl)
                if len(csl) == 2:
                    am, an = bg(pl, st, bh)
                    ds, pr = dij(am, csl[0], len(an))
                    if pr[csl[1]] != -1:  # Path exists
                        pi = gp(pr, csl[0], csl[1])
                        if pi:
                            pn = [an[i] for i in pi]
                            col = PC[cco % len(PC)]
                            cco += 1
                            spth.append((pn, col))
                    csl = []

    # Update all objects
    for p in pl:
        p.upd()
    for sat in st:
        sat.upd()
    for str in strs:
        str.upd(pl)

    # Draw black hole
    bh.draw(s)
    
    # Draw graph edges
    am, an = bg(pl, st, bh)
    for i in range(len(an)):
        for j in range(i + 1, len(an)):
            if am[i][j] < float("inf"):
                n1 = an[i]
                n2 = an[j]
                pygame.draw.line(
                    s, (60, 80, 220), (int(n1.x), int(n1.y)), (int(n2.x), int(n2.y)), 1
                )

    # Draw found paths
    for pn, col in spth:
        dp(s, pn, col)

    # Draw all objects
    for sat in st:
        sat.draw(s)
    for p in pl:
        p.draw(s)
    for str in strs:
        str.draw(s)

    # Draw UI text
    f = pygame.font.SysFont(None, 32)
    t = f.render("Click two objects to find shortest path", True, (200, 200, 255))
    s.blit(t, (20, 20))
    if csl:
        slt = f.render(f"Selected: {len(csl)}/2", True, (255, 200, 100))
        s.blit(slt, (20, 60))

    pygame.display.flip()
    c.tick(60)

pygame.quit()
