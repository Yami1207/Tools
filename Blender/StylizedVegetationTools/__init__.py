# -*- coding: utf-8 -*-

bl_info = {
    "name": "Stylized Vegetation Tools",
    "description": "风格化植被（烘焙AO、球形法线等）",
    "author": "Yami",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Stylized Vegetation Tools Panel",
    "category": "Object",
}

import bpy

from StylizedVegetationTools.Operators.FunctionOps import *
from StylizedVegetationTools.Operators.NormalOperator import *
from StylizedVegetationTools.Operators.AOOperator import *

from StylizedVegetationTools.Panels.FunctionPanel import *
from StylizedVegetationTools.Panels.NormalPanel import *
from StylizedVegetationTools.Panels.AOPanel import *

def register():
    bpy.utils.register_class(MatcapRenderOperator)
    bpy.utils.register_class(RenderVertexColorOperator)
    bpy.utils.register_class(NormalOperator)
    bpy.utils.register_class(AOOperator)

    bpy.utils.register_class(FunctionPanel)
    bpy.utils.register_class(NormalPanel)
    bpy.utils.register_class(AOPanel)

def unregister():
    bpy.utils.unregister_class(MatcapRenderOperator)
    bpy.utils.unregister_class(RenderVertexColorOperator)
    bpy.utils.unregister_class(NormalOperator)
    bpy.utils.unregister_class(AOOperator)

    bpy.utils.unregister_class(FunctionPanel)
    bpy.utils.unregister_class(NormalPanel)
    bpy.utils.unregister_class(AOPanel)

if __name__ == "__main__":
    register()
