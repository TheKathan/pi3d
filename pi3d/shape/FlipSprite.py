from pi3d.constants import *
from pi3d.Texture import Texture
from pi3d.Buffer import Buffer
from pi3d.shape.Sprite import Sprite

class FlipSprite(Sprite):
  """ 3d model inherits from Shape, differs from Plane in being single sided"""
  def __init__(self, camera=None, light=None, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=20.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0, flip=True):
    """Uses standard constructor for Shape. Extra Keyword arguments:

      *w*
        Width.
      *h*
        Height.
      *flip* Should the image be flipped over
    """
    #super(FlipSprite, self).super(Sprite, self).
    sprt = super(FlipSprite, self)
    super(Sprite, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                 sx, sy, sz, cx, cy, cz)

    self.width = w
    self.height = h
    self.ttype = GL_TRIANGLES
    self.verts = []
    self.norms = []
    self.texcoords = []
    self.inds = []

    ww = w / 2.0
    
 ###...
    hh = h / 2.0 if not flip else -h / 2.0
#    hh = h / 2.0
 
    self.verts = ((-ww, hh, 0.0), (ww, hh, 0.0), (ww, -hh, 0.0), (-ww, -hh, 0.0))
    self.norms = ((0, 0, -1), (0, 0, -1),  (0, 0, -1), (0, 0, -1))
    self.texcoords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0 , 1.0))

###...
    self.inds = ((0, 1, 3), (1, 2, 3)) if not flip else ((3, 2, 0), (2, 1, 0))   
#    self.inds = ((0, 1, 3), (1, 2, 3))

    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, self.norms))        

  def repaint(self, t):
    self.draw()
