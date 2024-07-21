# -*- coding: utf-8 -*-
import bpy
from bpy.types import Panel

from StylizedVegetationTools.Operators.FunctionOps import *

from StylizedVegetationTools.Panels.BasePanel import *

class FunctionPanel(BasePanel, Panel):
    bl_idname = "OBJECT_PT_stylized_vegetation_tools_function_panel"
    bl_label = '功能'

    def draw(self, context: bpy.types.Context):
        viewOptionColumn = self.layout.column()
        viewOptionColumn.operator(MatcapRenderOperator.bl_idname, text = "Matcap Render")

        if context.active_object is not None:
            viewOptionColumn.operator(RenderVertexColorOperator.bl_idname, text = "Render Vertex Color")
