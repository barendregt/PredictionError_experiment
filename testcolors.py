from psychopy import visual,core,event,monitors
import numpy as np
import ColorTools as ct
import psychopy.visual.shaders as shaders
import colorsys as cs


from IPython import embed as shell

params = {}				
params['monitor_width'] = 33
params['monitor_viewdist'] = 65
params['monitor_pixelDims'] = (2560, 1440)
params['screenSize'] = (2560, 1440)		

mon = monitors.Monitor(name = 'dell', width = params['monitor_width'], distance = params['monitor_viewdist'])
mon.setSizePix(params['monitor_pixelDims'])

screen = visual.Window(params['screenSize'], units = 'deg', monitor = mon, color = (1,1,1), allowGUI = False)

colorToBlackFragmentShader = '''
   uniform sampler2D texture, mask;
   void main() {
	   vec4 textureFrag = texture2D(texture,gl_TexCoord[0].st);
	   vec4 maskFrag = texture2D(mask,gl_TexCoord[1].st);
	   gl_FragColor.a = gl_Color.a*maskFrag.a*textureFrag.a;
	   gl_FragColor.rgb = gl_Color.rgb * ((textureFrag.rgb +1.0)/2.0);
   }
   '''
if screen.winType=='pyglet' and screen._haveShaders:
   screen._progSignedTexMask = shaders.compileProgram(shaders.vertSimple,
colorToBlackFragmentShader)
#end 				

base_lum = 55#0.5
# base_sat = 1.0

orientations = 45#np.linspace(90.0, 270.0, 9)
# orientations = orientations[0:7]
colors = np.linspace(0.0, 1.0, 9)
colors = colors[0:7]	 

color_theta = (np.pi*2)/8
color_angle = color_theta * np.arange(0.1,8.1,dtype=float)
color_radius = 80

color_a = color_radius * np.cos(color_angle)
color_b = color_radius * np.sin(color_angle)

# shell()

colors = [ct.lab2psycho((base_lum, a, b)) for a,b in zip(color_a, color_b)]

# colors = ((70, -80, 0),
# 		  (70, -50, 50),
# 		  (70, 0, 80),
# 		  (70, 50, 50),
# 		  (70, 80, 0),
# 		  (70, 50, -50),
# 		  (70, 0, -80),
# 		  (70, -50, -50)


# orientations = np.tile(orientations,(8,1))
# colors = np.tile(colors,(8,1))

xpos = np.linspace(-6.0, 6.0, 8)
ypos = 0.0#np.linspace(-6.0, 6.0, 8)

# stim_array = visual.ElementArrayStim(screen, elementTex = 'sqr', elementMask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, nElements = 64, sizes = 1.5, sfs = 1.0, xys = [[(x,y) for x in xpos] for y in ypos], oris = orientations, colors = colors, colorSpace = 'rgb') 

stim_array = []

for o, y in zip(orientations, ypos):
	for c, x in zip(colors, xpos):
		#stim_array.append(visual.GratingStim(screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = 1.0, ori = o,  size = 1.5, pos = (x,y), colorSpace = 'rgb255', color = [rgbc*255.0 for rgbc in cs.hls_to_rgb(c,base_lum,base_sat)]))
		stim_array.append(visual.GratingStim(screen, tex = 'sqr', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = 3.0, ori = o,  size = 1.0, pos = (x,y), colorSpace = 'rgb', color = c))

for stim in stim_array:
	stim.draw()

# stim_array.draw()
screen.flip()

event.waitKeys()

screen.close()
# # HSL colorlist
# colorlist = ((1,-1,-1),
# 			 (1,1,-1),
# 			 (-1,1,-1),
# 			 (-1,1,1),
# 			 (-1,-1,1),
# 			 (1,-1,1)