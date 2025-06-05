import bpy
import os
import glob
import sys
import random
import math
import argparse
parser = argparse.ArgumentParser()
args, extra = parser.parse_known_args()
parser.add_argument("--input_dir", default="")
parser.add_argument("--save_dir",default="")

args = parser.parse_args()

current_directory = os.path.dirname(os.path.abspath(__file__))

if current_directory not in sys.path:
    sys.path.append(current_directory)

task=7

input_dir = args.input_dir
fbx_dir = args.save_dir
if not os.path.exists(fbx_dir):
    os.makedirs(fbx_dir)
img_dir = args.save_dir
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

glb_files = glob.glob(os.path.join(input_dir, '*.glb'))

for glb_file in glb_files:
    name = glb_file.split('/')[-1].split('.')[0]

    # clear other objects
    bpy.ops.wm.read_factory_settings(use_empty=True)

    #import glb
    import logging
    logging.disable(logging.DEBUG)
    
    try:
        # First attempt: Import without any optional parameters that might trigger debug logging
        bpy.ops.import_scene.gltf(filepath=glb_file)
    except Exception as e:
        print(f"GLTF import failed with basic parameters for {glb_file}: {e}")
        
        # Second attempt: Try to set Blender app debug value to prevent logging issues
        try:
            original_debug = bpy.app.debug_value
            bpy.app.debug_value = 0
            bpy.ops.import_scene.gltf(filepath=glb_file)
            bpy.app.debug_value = original_debug
        except Exception as e2:
            print(f"GLTF import failed with debug disabled for {glb_file}: {e2}")
            logging.disable(logging.NOTSET)
            continue
    
    # Re-enable logging
    logging.disable(logging.NOTSET)

    for material in bpy.data.materials:
        if not material.node_tree:
            continue

        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                image = node.image
                
                image_path = os.path.join(fbx_dir, name + ".png")
                image.filepath_raw = image_path
                image.file_format = 'PNG'
                image.save()
                print(f"Saved: {image_path}")

    
    fbx_path = os.path.join(fbx_dir,f"{name}.obj")
    bpy.ops.export_scene.obj(
            filepath=fbx_path, 
            use_selection=False, 
            use_materials=True,
            )
