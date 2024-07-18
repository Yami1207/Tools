# -*- coding: utf-8 -*-
import bpy
from bpy.types import Panel

from StylizedVegetationTools.Operators.NormalOperator import *

from StylizedVegetationTools.Panels.BasePanel import *

class NormalPanel(BasePanel, Panel):
    bl_idname = "OBJECT_PT_stylized_vegetation_tools_normal_panel"
    bl_label = '法线'

    def draw(self, context: bpy.types.Context):
        activeObject = context.active_object
        if activeObject is None:
            self.layout.label(text='Select a Model')
        else:
            optionColumn = self.layout.column()
            optionColumn.operator(NormalOperator.bl_idname, text = "修正法线")
