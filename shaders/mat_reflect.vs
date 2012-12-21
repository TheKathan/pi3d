precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;
uniform mat4 cameraviewmatrix;
uniform vec3 unib[2];
//uniform float ntiles => unib[0][0]
uniform vec3 unif[11];
//uniform vec3 lightpos > unif[8]

varying vec3 normout;
varying vec2 bumpcoordout;
varying vec2 shinecoordout;
varying mat4 normrot;
varying float dist;
varying vec3 lightVector;

void main(void) {
  
  lightVector = normalize(vec3(cameraviewmatrix * vec4(unif[8], 0.0))); // ------ rotate relative to view
  //lightVector = normalize(unif[8]);
  normout = normalize(vec3(modelviewmatrix * vec4(normal, 0.0)));   

  vec3 bnorm = vec3(0.0, 0.0, 1.0); // ----- normal to original bump map sheet
  float c = dot(bnorm, normout); // ----- cosine
  float t = 1.0 - c;
  vec3 a = cross(bnorm, normout); // ----- axis
  float s = length(a); // ----- sine (depends on bnorm and normout being unit vectors)
  //if (s > 0.0) a = normalize(a);
  a = normalize(a);
  normrot = mat4(
    t * a.x * a.x + c, t * a.x * a.y + a.z * s, t * a.x * a.z - a.y * s, 0.0,
    t * a.x * a.y - a.z * s, t * a.y * a.y + c, t * a.z * a.y + a.x * s, 0.0,
    t * a.x * a.z + a.y * s, t * a.y * a.z - a.x * s, t * a.z * a.z + c, 0.0,
    0.0, 0.0, 0.0, 1.0); // ----- vector mult for rotation about axis
  bumpcoordout = texcoord * unib[0][0];

  vec3 inray = vertex - vec3(modelviewmatrix * vec4(unif[6], 1.0)); // ----- vector from the camera to this vertex TODO should use camerviewmatrix
  //if (length(inray) > 0.0) inray = normalize(inray); // ----- crash if normalize zero length vectors
  inray = normalize(inray);
  vec3 refl = reflect(inray, normout); // ----- reflection direction from this vertex
  vec3 horiz = cross(inray, vec3(0.0, 1.0, 0.0)); // ----- a 'horizontal' unit vector normal to the inray
  vec3 vert = cross(inray, vec3(1.0, 0.0, 0.0)); // ----- a 'vertical' unit vector normal to the inray
  float hval = dot(refl, horiz); // ----- component of the reflected ray along horizonal
  float vval = dot(refl, vert); // -----  componet of reflected ray along vertical
  float zval = dot(refl, -1.0 * inray); // ----- component of reflected ray in direction back to camera
  // ----- now work out the horizonal and vertical angles relative to inray and map them to range 0 to 1
  shinecoordout = vec2(clamp(0.5 - atan(hval, zval)/6.283185307, 0.0, 1.0), clamp(0.5 - atan(vval, zval)/6.283185307, 0.0, 1.0));

  vec4 relPosn = modelviewmatrix * vec4(vertex,1.0);
  dist = length(relPosn);
  gl_Position = relPosn;
}
