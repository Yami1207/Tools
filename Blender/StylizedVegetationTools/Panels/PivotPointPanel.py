# -*- coding: utf-8 -*-
import bpy
from bpy.types import Panel

from StylizedVegetationTools.Operators.PivotPointOperator import *

from StylizedVegetationTools.Panels.BasePanel import *

class PivotPointPanel(BasePanel, Panel):
    bl_idname = "OBJECT_PT_stylized_vegetation_tools_pivot_point_panel"
    bl_label = '植被轴心点'

    def draw(self, context: bpy.types.Context):
        count = len(context.selected_objects)
        if count == 0:
            self.layout.label(text = '选择物体')
        else:
            self.layout.label(text = '写入轴心点到UV数据')
            self.layout.label(text = '注意：数据需要占用2个uv保存')

            optionColumn = self.layout.column()
            optionColumn.operator(PivotPointOperator.bl_idname, text = "写入轴心点")
