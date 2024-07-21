# -*- coding: utf-8 -*-
import bpy
from bpy.types import Panel

from StylizedVegetationTools.Operators.NormalOperator import *
from StylizedVegetationTools.Operators.FunctionOps import *

from StylizedVegetationTools.Panels.BasePanel import *

class NormalPanel(BasePanel, Panel):
    bl_idname = "OBJECT_PT_stylized_vegetation_tools_normal_panel"
    bl_label = '法线'

    def draw(self, context: bpy.types.Context):
        if bpy.context.object.mode != "OBJECT":
            viewOptionColumn = self.layout.column()
            viewOptionColumn.operator(MatcapRenderOperator.bl_idname, text = "切换到物体模式")
        else:
            activeObject = context.active_object
            if activeObject is None:
                self.layout.label(text = 'Select a Model')
            else:
                optionColumn = self.layout.column()
                optionColumn.operator(NormalOperator.bl_idname, text = "修正法线")
