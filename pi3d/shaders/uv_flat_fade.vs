#include std_head_vs.inc

varying vec2 texcoordout;
varying float dist;
varying float fade_dist;

void main(void) {
  texcoordout = texcoord * unib[2].xy + unib[3].xy;
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  dist = gl_Position.z;
  gl_PointSize = unib[2][2] / dist;
  fade_dist = length(gl_Position.xy);
}
