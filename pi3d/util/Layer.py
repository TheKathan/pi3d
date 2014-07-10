import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Camera import Camera
from pi3d.shape.FlipSprite import FlipSprite
from pi3d.Display import Display

class Layer(OffScreenTexture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self, camera, shader=None, blend=True, mipmap=False, flip=False, z=1):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """   
    super(Layer, self).__init__("Layer")
    
    self.sprite = FlipSprite(camera=camera, w=Display.INSTANCE.width, h=Display.INSTANCE.height, z=z, flip=True)
    
    # load shader for casting shadows and camera
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

