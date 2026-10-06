import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'assets/models'
for p in sorted(root.glob('*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(p))
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 assert meshes and all(len(o.data.vertices)>0 for o in meshes)
 assert all(o.animation_data is None for o in meshes)
 q=p.with_suffix('.glb');assert q.read_bytes()[:4]==b'glTF'
 print('VERIFIED',p.name,len(meshes),'meshes',flush=True)
