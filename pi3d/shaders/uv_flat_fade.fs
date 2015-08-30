#include std_head_fs.inc

varying vec2 texcoordout;
varying float dist;
varying float fade_dist;

void main(void) {
#include std_main_uv.inc
  gl_FragColor = (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a *= (1.75 - fade_dist) * (1.75 - fade_dist) * 1.5;
}


