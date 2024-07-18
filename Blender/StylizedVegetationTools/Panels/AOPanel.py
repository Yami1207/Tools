import bpy
from bpy.types import Panel

from StylizedVegetationTools.Operators.AOOperator import *

from StylizedVegetationTools.Panels.BasePanel import *

class AOPanel(BasePanel, Panel):
    bl_idname = "OBJECT_PT_stylized_vegetation_tools_ao_panel"
    bl_label = 'AO'

    def draw(self, context: bpy.types.Context):
        optionColumn = self.layout.column()
        optionColumn.operator(AOOperator.bl_idname, text = "烘焙AO")
