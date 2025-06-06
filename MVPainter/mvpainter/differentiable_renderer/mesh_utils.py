# Open Source Model Licensed under the Apache License Version 2.0
# and Other Licenses of the Third-Party Components therein:
# The below Model in this distribution may have been modified by THL A29 Limited
# ("Tencent Modifications"). All Tencent Modifications are Copyright (C) 2024 THL A29 Limited.

# Copyright (C) 2024 THL A29 Limited, a Tencent company.  All rights reserved.
# The below software and/or models in this distribution may have been
# modified by THL A29 Limited ("Tencent Modifications").
# All Tencent Modifications are Copyright (C) THL A29 Limited.

# Hunyuan 3D is licensed under the TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT
# except for the third-party components listed below.
# Hunyuan 3D does not impose any additional limitations beyond what is outlined
# in the repsective licenses of these third-party components.
# Users must comply with all terms and conditions of original licenses of these third-party
# components and must ensure that the usage of the third party components adheres to
# all relevant laws and regulations.

# For avoidance of doubts, Hunyuan 3D means the large language models and
# their software and algorithms, including trained model weights, parameters (including
# optimizer states), machine-learning model code, inference-enabling code, training-enabling code,
# fine-tuning enabling code and other elements of the foregoing made publicly available
# by Tencent in accordance with TENCENT HUNYUAN COMMUNITY LICENSE AGREEMENT.

import trimesh
import numpy as np


def load_mesh(mesh):
    vtx_pos = mesh.vertices if hasattr(mesh, 'vertices') else None
    pos_idx = mesh.faces if hasattr(mesh, 'faces') else None

    vtx_uv = mesh.visual.uv if hasattr(mesh.visual, 'uv') else None
    uv_idx = mesh.faces if hasattr(mesh, 'faces') else None

    # Validate and fix UV coordinates if they exist
    if vtx_uv is not None:
        # Check for NaN or infinite values
        if np.any(np.isnan(vtx_uv)) or np.any(np.isinf(vtx_uv)):
            print("Warning: Invalid UV coordinates detected in mesh. Cleaning up...")
            
            # Replace NaN/inf values with valid UV coordinates
            vtx_uv = np.where(np.isfinite(vtx_uv), vtx_uv, 0.5)
            
            # Clamp UV coordinates to valid range [0, 1]
            vtx_uv = np.clip(vtx_uv, 0.0, 1.0)
            
            print(f"UV coordinates cleaned. Shape: {vtx_uv.shape}")
        
        # Ensure UV coordinates are in valid range
        if np.any((vtx_uv < 0.0) | (vtx_uv > 1.0)):
            print("Warning: UV coordinates out of range [0,1]. Clamping...")
            vtx_uv = np.clip(vtx_uv, 0.0, 1.0)

    texture_data = None

    return vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data


def save_mesh(mesh, texture_data):
    material = trimesh.visual.texture.SimpleMaterial(image=texture_data, diffuse=(255, 255, 255))
    texture_visuals = trimesh.visual.TextureVisuals(uv=mesh.visual.uv, image=texture_data, material=material)
    mesh.visual = texture_visuals
    return mesh
