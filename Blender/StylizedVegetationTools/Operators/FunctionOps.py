# -*- coding: utf-8 -*-
import bpy

class MatcapRenderOperator(bpy.types.Operator):
    bl_idname = "stylized_vegetation_tools.matcap_render_operator"
    bl_label = 'Matcap Render'

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode = "OBJECT", toggle = False)
        context.space_data.shading.type = 'SOLID'
        context.space_data.shading.light = 'MATCAP'
        context.space_data.shading.studio_light = 'check_normal+y.exr'
        return {"FINISHED"}

class RenderVertexColorOperator(bpy.types.Operator):
    bl_idname = "stylized_vegetation_tools.render_vertex_color_operator"
    bl_label = 'Render Vertex Color'

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        context.space_data.shading.light = 'FLAT'
        bpy.ops.object.mode_set(mode = "VERTEX_PAINT", toggle = False)
        return {"FINISHED"}
