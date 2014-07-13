import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Camera import Camera
from pi3d.shape.FlipSprite import FlipSprite
from pi3d.Display import Display

class Layer(OffScreenTexture):
  """An off screen texture with a full screen sprite at a user defined depth
  Used for drawing foreground shapes once and using over repeated frames.
  Warning: Using DISPLAY.set_background() will also set the background colour of 
  this layer.  Make the display background transparent and add a background layer"""
  
  def __init__(self, camera, shader=None, flip=True, w=None, h=None, z=1):
    """Camera must be a 2d camera. Extra Keyword arguments:

      *flip* Should the image be flipped over
      *w* and *h* default to display size if not defined
      *center* put the sprite at the full screen center. The main display must be initialized first if using 
    """
        
    from pi3d.Display import Display
    scrnheight = Display.INSTANCE.height
    scrnwidth = Display.INSTANCE.width
        
    if w==None:
        width = Display.INSTANCE.width
    else:
        width = w
            
    if h==None:
        height = Display.INSTANCE.height
    else:
        height = h
            
    self.xoffset = int((width - scrnwidth) * 0.5)
    self.yoffset = int((height - scrnheight) * 0.5)

    super(Layer, self).__init__("Layer", w, h)    
    self.sprite = FlipSprite(camera=camera, w=self.ix, h=self.iy, z=z, flip=True)
    
    # If not defined, load shader for drawing layer
    if shader==None:
        self.shader = Shader("uv_flat")
    else:
        self.shader = shader
        

  def start_layer(self):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. If you want blurred
    edges you will have to capture the rendering of an object and its
    background then re-draw them using the blur() method. Large objects
    will obviously take a while to draw and re-draw
    """
    super(Layer, self)._start()

  def end_layer(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    super(Layer, self)._end()

    
  def draw_layer(self):
    self.sprite.draw(self.shader, [self])

