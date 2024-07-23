# -*- coding: utf-8 -*-
import bpy
import math, mathutils

class PivotPointOperator(bpy.types.Operator):
    bl_idname = "stylized_vegetation_tools.pivot_point_operator"
    bl_label = 'Pivot Point'

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        for obj in bpy.context.selected_objects:
            # 获取描点
            p = self.GetOrigin(obj)
            
            mesh = obj.data
            pivotPointXY = self.GetOrNewLayerIndex(mesh.uv_layers, "PivotPointXY")
            pivotPointZ = self.GetOrNewLayerIndex(mesh.uv_layers, "PivotPointZ")
            if pivotPointXY != -1 and pivotPointZ != -1:
                for poly in mesh.polygons:
                    for index in poly.loop_indices:
                        mesh.uv_layers[pivotPointXY].data[index].uv = (p.x, p.y)
                        mesh.uv_layers[pivotPointZ].data[index].uv = (p.z, 0)

        return {"FINISHED"}
    
    def GetOrNewLayerIndex(self, layers, name):
        index = -1
        try:
            layerNames = [ l.name for l in layers ]
            index = layerNames.index(name)
        except ValueError:
            index = len(layerNames)
            layers.new(name = name)
        return index
        
    def GetOrigin(self, obj):
        # 缩放
        scale = obj.matrix_world.to_scale()
        vec1 = mathutils.Vector((obj.bound_box[0][0] * scale[0], obj.bound_box[0][1] * scale[1], obj.bound_box[0][2] * scale[2]))
        vec2 = mathutils.Vector((obj.bound_box[6][0] * scale[0], obj.bound_box[6][1] * scale[1], obj.bound_box[6][2] * scale[2]))
        center = 0.5 * (vec1 + vec2)

        # 旋转
        rotation = obj.matrix_world.to_euler('XYZ')
        center.rotate(rotation)
	    
        # 平移
        center = obj.matrix_world.to_translation() + center
        return center
