import pygame, math, random
pygame.init()
width = 800
height = 600
cx = width//2
cy = height//2
fov = min(width,height)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Game Engine')
clock = pygame.time.Clock()
crashed = False

def rotate2d(pos,rad): x,y=pos; s,c = math.sin(rad),math.cos(rad); return x*c-y*s,y*c+x*s

class Cam:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
    def events(self,event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x/=200
            y/=200
            self.rot[0]-=y
            self.rot[1]+=x
    def update(self,dt,key):
        s = dt*10
        if key[pygame.K_SPACE]: self.pos[1]+=s
        if key[pygame.K_LSHIFT]: self.pos[1]-=s
        x,y = s*math.sin(self.rot[1]),s*math.cos(self.rot[1])
        if key[pygame.K_w]: self.pos[0]+=x; self.pos[2]+=y
        if key[pygame.K_s]: self.pos[0]-=x; self.pos[2]-=y
        if key[pygame.K_a]: self.pos[0]-=y; self.pos[2]+=x
        if key[pygame.K_d]: self.pos[0]+=y; self.pos[2]-=x

class tri(object):
    def __init__(self,pos1=(0,0,0),pos2=(0,0,0),pos3=(0,0,0)):
        self.points = [pos1,pos2,pos3]
        self.points2d = []

class box(object):
    def __init__(self,w,l,h,pos=(0,0,0)):
        self.pos = pos
        x = pos[0]
        y = pos[1]
        z = pos[2]
        self.mesh = []
        self.mesh.append(tri((0+x,0+y,0+z),(0+x,1+y+h,0+z),(1+x+w,1+y+h,0+z)))
        self.mesh.append(tri((0+x,0+y,0+z),(1+x+w,1+y+h,0+z),(1+x,0+y,0+z)))
        self.mesh.append(tri((1+x+w,0+y,0+z),(1+x+w,1+y+h,0+z),(1+x+w,1+y+h,1+z+l)))
        self.mesh.append(tri((1+x+w,0+y,0+z),(1+x+w,1+y+h,1+z+l),(1+x+w,0+y,1+z+l)))
        self.mesh.append(tri((1+x+w,0+y,1+z+l),(1+x+w,1+y+h,1+z+l),(0+x,1+y+h,1+z+l)))
        self.mesh.append(tri((1+x+w,0+y,1+z+l),(0+x,1+y+h,1+z+l),(0+x,0+y,1+z+l)))
        self.mesh.append(tri((0+x,0+y,1+l+z),(0+x,1+y+h,1+z+l),(0+x,1+y+h,0+z)))
        self.mesh.append(tri((0+x,0+y,1+l+z),(0+x,1+y+h,0+z),(0+x,0+y,0+z)))
        self.mesh.append(tri((0+x,1+y+h,0+z),(0+x,1+y+h,1+z+l),(1+x+w,1+y+h,1+z+l)))
        self.mesh.append(tri((0+x,1+y+h,0+z),(1+x+w,1+y+h,1+z+l),(1+x+w,1+y+h,0+z)))
        self.mesh.append(tri((0+x,0+y,0+z),(0+x,0+y,1+z+l),(1+x+w,0+y,1+z+l)))
        self.mesh.append(tri((0+x,0+y,0+z),(1+x+w,0+y,1+z+l),(1+x+w,0+y,0+z)))

class triangle(object):
    def __init__(self,pos=(0,0,0)):
        self.pos = pos
        self.mesh = [tri((0+pos[0],0+pos[1],0+pos[2]),(0+pos[0],1+pos[1],0+pos[2]),(1+pos[0],1+pos[1],0+pos[2]))]
shapes = [box(0,0,0,(0,0,0))]
cam = Cam((0,0,-5))
pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)
while not crashed:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(1); pygame.event.set_grab(0)
                crashed = True
        cam.events(event)
    screen.fill((255,255,255))
    for shape in shapes:
        colour = 0
        for tri in shape.mesh:
            colour += 1
            points = []
            for x,y,z in tri.points:
                x -= cam.pos[0]
                y -= cam.pos[1]
                z -= cam.pos[2]
                x,z = rotate2d((x,z),cam.rot[1])
                y,z = rotate2d((y,z),cam.rot[0])
                f = fov/z
                x,y = x*f,y*f
                points += [(cx+int(x),cy+int(y)*-1)]
            pygame.draw.polygon(screen,(75,75,75),points,1)
    key = pygame.key.get_pressed()
    cam.update(dt,key)
    pygame.display.flip()
pygame.quit()
