import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Camera import Camera
from pi3d.shape.Plane import Plane

class Layer(OffScreenTexture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self, file, camera, shader=None, blend=True, mipmap=False):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    
    super(Layer, self).__init__("Layer")
    
    self.camera = camera
    self.surface = Plane(camera=camera, w=self.ix, h=self.iy, z=1)
    self.alpha = False
    self.blend = True
    self.mipmap= mipmap
    self.tex_list = [self] # TODO check if this self reference causes graphics memory leaks
    
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
    opengles.glClearColor(ctypes.c_float(0.0), ctypes.c_float(0.0), 
                        ctypes.c_float(0.0), ctypes.c_float(0.0))
    super(Layer, self)._start()
#    self.camera.reset(is_3d=False)
#    self.location = (0,0,0)
#    self.camera.position(self.location)

  def end_layer(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    opengles.glClearColor(ctypes.c_float(0.0), ctypes.c_float(0.0), 
                        ctypes.c_float(0.0), ctypes.c_float(0.0))    
    super(Layer, self)._end()
    # change background back to blue
#    opengles.glClearColor(ctypes.c_float(0.4), ctypes.c_float(0.8), 
#                        ctypes.c_float(0.8), ctypes.c_float(1.0))

    
  def draw_layer(self):
    self.surface.draw(shader=self.shader, camera=self.camera, txtrs=[self], ntl=0, shny=0)
#    self.surface.draw(self.shader, [self], 0.0, 0.0)
