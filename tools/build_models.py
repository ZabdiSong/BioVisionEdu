"""Run with Blender 4.2+: blender --background --python tools/build_models.py.
Creates editable educational schematics, GLB exports and an offline web mesh bundle.
No animation or molecular-coordinate claims are included.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/models';OUT.mkdir(parents=True,exist_ok=True)
MODELS={}
PALETTE={'teal':(0.12,.61,.55,1),'green':(.36,.71,.42,1),'lime':(.69,.86,.39,1),'gold':(.94,.68,.25,1),'blue':(.28,.51,.79,1),'pink':(.89,.48,.57,1),'purple':(.60,.43,.76,1),'coral':(.90,.39,.29,1),'white':(.88,.93,.91,1)}

def reset():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 for data in list(bpy.data.materials):bpy.data.materials.remove(data)

def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True
 bsdf=m.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=color;bsdf.inputs['Roughness'].default_value=.38;bsdf.inputs['Alpha'].default_value=color[3]
 return m

def finish(o,name,key,mat,desc):
 o.name=name;o['part_id']=key;o['description']=desc;o.data.materials.append(mat)
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 return o

def sphere(name,key,loc,scale,color,desc,segments=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=12,location=loc)
 o=bpy.context.object;o.scale=scale
 return finish(o,name,key,material(name,color),desc)

def cylinder(name,key,loc,radius,depth,color,desc,rotation=(0,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=radius,depth=depth,location=loc,rotation=rotation)
 return finish(bpy.context.object,name,key,material(name,color),desc)

def box(name,key,loc,scale,color,desc):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale
 bevel=o.modifiers.new('Soft edges','BEVEL');bevel.width=.14;bevel.segments=3
 return finish(o,name,key,material(name,color),desc)

def tube(name,key,points,rad,color,desc):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=rad;c.bevel_resolution=3
 sp=c.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.select_set(False)
 return finish(o,name,key,material(name,color),desc)

def join(parts,name,key,color,desc):
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object
 return finish(o,name,key,material(name,color),desc)

def camera_and_lights():
 bpy.ops.object.camera_add(location=(9,-13,10));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,0))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=13;bpy.context.scene.camera=camera
 for loc,power,size in [((0,-7,9),1800,8),((6,4,6),1100,7),((-6,2,5),900,6)]:
  bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,0))-light.location).to_track_quat('-Z','Y').to_euler()
 bpy.context.scene.world.color=(.14,.17,.18);bpy.context.scene.render.engine='BLENDER_EEVEE_NEXT'
 bpy.context.scene.render.resolution_x=1200;bpy.context.scene.render.resolution_y=800;bpy.context.scene.render.resolution_percentage=100


def save(model_id,title,description):
 camera_and_lights();bpy.context.scene['educational_note']='Schematic, not to scale; simplified protein shapes; no animation.'
 bpy.context.scene['model_description']=description
 meshes=[]
 for obj in bpy.context.scene.objects:
  if obj.type!='MESH' or 'part_id' not in obj:continue
  deps=bpy.context.evaluated_depsgraph_get();evalobj=obj.evaluated_get(deps);mesh=evalobj.to_mesh();mesh.calc_loop_triangles()
  points=[]
  for v in mesh.vertices:
   p=obj.matrix_world@v.co;points.extend([round(p.x,5),round(p.z,5),round(-p.y,5)])
  triangles=[i for t in mesh.loop_triangles for i in t.vertices]
  c=list(obj.data.materials[0].diffuse_color) if len(obj.data.materials) else list(PALETTE['teal'])
  meshes.append({'id':obj['part_id'],'name':obj.name,'description':obj.get('description',''),'color':c,'positions':points,'indices':triangles})
  evalobj.to_mesh_clear()
 MODELS[model_id]={'name':title,'description':description,'parts':meshes}
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{model_id}.blend'))
 bpy.ops.export_scene.gltf(filepath=str(OUT/f'{model_id}.glb'),export_format='GLB',export_cameras=False,export_lights=False,export_extras=True,export_animations=False)
 print('MODEL_READY',model_id,len(meshes),flush=True)

reset()
sphere('Outer membrane','outer',(0,0,0),(3.6,1.65,1.45),(.90,.48,.30,.22),'Outer boundary of the mitochondrion; proteins and pores are simplified.',48)
sphere('Inner membrane','inner',(0,0,0),(3.30,1.38,1.20),(.88,.67,.38,.20),'Inner membrane encloses the matrix; cristae are folds of this membrane.',48)
sphere('Matrix region','matrix',(0,0,0),(3.05,1.15,1.0),(.95,.80,.53,.11),'Pyruvate oxidation and most citric acid cycle reactions occur in the matrix.',32)
cristae=[]
for x in [-2.4,-1.6,-.8,0,.8,1.6,2.4]:
 width=1.05*math.sqrt(max(.15,1-(x/3.1)**2))
 pts=[(x+.18*math.sin(i*math.pi/30),width*math.cos(i*math.pi/30),.8*math.sin(i*math.pi/30)) for i in range(61)]
 cristae.append(tube('Crista','cristae',pts,.055,PALETTE['gold'],'Cristae increase inner membrane area.'))
join(cristae,'Cristae folds','cristae',PALETTE['gold'],'Folds provide membrane area for electron transport and ATP synthesis.')
for i,x in enumerate([-1.6,0,1.6]):
 cylinder('ATP synthase stalk '+str(i),'atp-synthase',(x,-.85,.45),.06,.36,PALETTE['blue'],'ATP synthase links proton flow to ATP production.')
 sphere('ATP synthase head '+str(i),'atp-synthase',(x,-.85,.69),(.18,.18,.14),PALETTE['blue'],'Catalytic head projects into the matrix; placement is schematic.')
tube('Mitochondrial DNA','dna',[(-1+.35*math.cos(i*2*math.pi/40),.2+.35*math.sin(i*2*math.pi/40),-.35) for i in range(41)],.035,PALETTE['teal'],'Mitochondria contain their own DNA; this loop is a schematic.')
save('mitochondrion','Mitochondrion','Double membranes, matrix, cristae and ATP synthase. Transparent envelopes expose the interior.')

reset()
sphere('Outer envelope','outer',(0,0,0),(3.6,1.8,1.30),(.16,.56,.34,.22),'The chloroplast has an outer and an inner envelope membrane.',48)
sphere('Inner envelope','inner',(0,0,0),(3.35,1.58,1.10),(.48,.75,.35,.14),'The inner envelope encloses the stroma.',48)
sphere('Stroma','stroma',(0,0,0),(3.1,1.35,.95),(.72,.84,.54,.12),'The Calvin cycle occurs in the stroma, outside the thylakoid lumen.')
for j,(x,y) in enumerate([(-2,-.2),(0,.4),(2,-.2)]):
 parts=[]
 for z in [-.50,-.30,-.10,.10,.30,.50]:parts.append(cylinder('Thylakoid','granum-'+str(j),(x,y,z),.66,.11,PALETTE['green'],'Thylakoid membrane surrounds a lumen; stacks are called grana.'))
 join(parts,'Granum '+str(j+1),'granum-'+str(j),PALETTE['green'],'Stacked thylakoids organize light-reaction membranes. Lumen is inside each disc.')
box('Stroma lamella left','lamella',(-1,.1,0),(1.4,.24,.08),PALETTE['teal'],'Lamellae connect thylakoid stacks.')
box('Stroma lamella right','lamella',(1,.1,0),(1.4,.24,.08),PALETTE['teal'],'Lamellae connect thylakoid stacks.')
tube('Chloroplast DNA','dna',[(-.6+.25*math.cos(i*2*math.pi/32),-.8+.25*math.sin(i*2*math.pi/32),-.55) for i in range(33)],.035,PALETTE['gold'],'Chloroplast DNA is shown schematically.')
save('chloroplast','Chloroplast','Envelope, stroma, grana and lamellae. Light reactions occur in thylakoid membranes; the Calvin cycle occurs in the stroma.')


def membrane():
 parts=[]
 for x in [i*.4-5 for i in range(26)]:
  for y in [-.58,.58]:
   for z in [-.30,.30]:
    parts.append(sphere('Lipid head','bilayer',(x,y,z),(.16,.16,.13),PALETTE['lime'],'Hydrophilic head of a schematic phospholipid.',12))
    parts.append(cylinder('Lipid tails','bilayer',(x,y,z/2),.035,.25,PALETTE['gold'],'Hydrophobic core limits free proton movement.'))
 join(parts,'Phospholipid bilayer','bilayer',PALETTE['lime'],'A selectively permeable membrane separates two compartments.')

def proton_cloud():
 parts=[]
 for x,z in [(-4,1.5),(-3,1.7),(-2,1.9),(-1,1.5),(0,1.8),(1,1.7),(2,1.9),(3,1.6),(4,1.8)]:parts.append(sphere('Proton','protons',(x,.3,z),(.13,.13,.13),PALETTE['pink'],'H+ concentration is higher on this side of the membrane.',12))
 join(parts,'Protons on high-concentration side','protons',PALETTE['pink'],'A proton gradient stores electrochemical potential energy.')

def atp_synthase(x):
 cylinder('ATP synthase channel','atp-synthase',(x,0,0),.34,.85,PALETTE['blue'],'Protons return across the membrane through ATP synthase.')
 cylinder('ATP synthase stalk','atp-synthase',(x,0,-.72),.10,.55,PALETTE['blue'],'The stalk couples proton-driven rotation to the catalytic head.')
 sphere('ATP synthase catalytic head','atp-synthase',(x,0,-1.14),(.48,.48,.33),PALETTE['blue'],'The F1 head faces the matrix or stroma, where ATP is synthesized.')

reset();membrane();proton_cloud()
box('Complex I','complex-i',(-4,0,-.25),(.85,.9,1.7),PALETTE['purple'],'Accepts electrons from NADH and pumps protons from matrix to intermembrane space.')
box('Complex II','complex-ii',(-2.8,-.48,-.35),(.55,.50,.85),PALETTE['teal'],'Feeds electrons from succinate via FAD to ubiquinone; does not pump protons.')
sphere('Ubiquinone Q','q',(-2,0,0),(.23,.23,.23),PALETTE['coral'],'A mobile lipid-soluble electron carrier in the membrane.')
box('Complex III','complex-iii',(-.65,0,0),(.9,.9,1.15),PALETTE['gold'],'Transfers electrons to cytochrome c and contributes to proton translocation.')
sphere('Cytochrome c','cytochrome-c',(.45,0,.85),(.19,.19,.19),PALETTE['coral'],'A mobile electron carrier on the intermembrane-space side.')
box('Complex IV','complex-iv',(1.65,0,0),(.9,.9,1.2),PALETTE['pink'],'Transfers electrons to oxygen, forming water; contributes to proton pumping.')
atp_synthase(4)
tube('Electron route','electron-route',[(-4,0,-.9),(-4,0,0),(-2,0,0),(-.65,0,0),(.45,0,.85),(1.65,0,0),(1.65,0,-.9)],.035,PALETTE['white'],'Electron transfer through carriers releases energy used to build a proton gradient.')
sphere('Oxygen acceptor','oxygen',(2.15,0,-1.05),(.20,.20,.20),PALETTE['coral'],'Oxygen is the terminal electron acceptor, reduced to water at complex IV.')
save('respiratory-etc','Respiratory electron transport chain','High-proton side is the intermembrane space; ATP synthase head faces the matrix. Complex II does not pump protons.')

reset();membrane();proton_cloud()
box('Photosystem II','psii',(-4,0,0),(.9,1,1.45),PALETTE['green'],'Light excites electrons; water oxidation supplies replacement electrons and releases oxygen.')
sphere('Plastoquinone','pq',(-2.5,0,0),(.23,.23,.23),PALETTE['coral'],'A mobile membrane carrier transports electrons toward cytochrome b6f.')
box('Cytochrome b6f','b6f',(-1,0,0),(.8,.9,1.2),PALETTE['gold'],'Electron transfer contributes to proton accumulation in the thylakoid lumen.')
sphere('Plastocyanin','pc',(.15,0,.8),(.18,.18,.18),PALETTE['blue'],'A mobile carrier transfers electrons toward photosystem I.')
box('Photosystem I','psi',(1.2,0,0),(.9,.9,1.4),PALETTE['purple'],'A second light excitation raises electron energy before NADP+ reduction.')
sphere('NADP+ reductase','fnr',(2.35,0,-.85),(.27,.3,.23),PALETTE['pink'],'On the stromal side, electrons ultimately reduce NADP+ to NADPH.')
atp_synthase(4)
tube('Electron route','electron-route',[(-4,0,.8),(-4,0,0),(-2.5,0,0),(-1,0,0),(.15,0,.8),(1.2,0,0),(2.35,0,-.85)],.035,PALETTE['white'],'Linear electron flow produces reducing power; chemiosmosis produces ATP.')
sphere('Water donor','water',(-4.7,0,.9),(.22,.22,.22),PALETTE['blue'],'Water supplies electrons to photosystem II; released O2 comes from water.')
save('light-reactions','Thylakoid light reactions','High-proton side is the thylakoid lumen; ATP synthase head and NADPH production face the stroma.')
(OUT/'model-data.js').write_text('window.BIOVISION_MODELS='+json.dumps(MODELS,separators=(',',':'))+';\n')
(OUT/'model-manifest.json').write_text(json.dumps({k:{'name':v['name'],'description':v['description'],'parts':len(v['parts']),'blend':k+'.blend','glb':k+'.glb'} for k,v in MODELS.items()},indent=2))
print('ALL_MODELS_READY',flush=True)
