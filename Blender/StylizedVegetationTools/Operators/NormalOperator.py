# -*- coding: utf-8 -*-
import bpy

from StylizedVegetationTools.Operators.Utils import *

class NormalOperator(bpy.types.Operator):
    bl_idname = "stylized_vegetation_tools.normal_operator"
    bl_label = 'Normal'

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        selectObject = context.view_layer.objects.active
        selectObject.select_set(True)

        # 复制mesh对象
        bpy.ops.object.duplicate(linked = False)
        extendObject = context.active_object
        extendObject.name = selectObject.name + "_ExtendMesh"
        extendObject.select_set(True)

        # 添加Geometry node modifier
        bpy.ops.object.modifier_add(type = 'NODES')
        geometryNodeModifier = extendObject.modifiers[-1]
        geometryNodeModifier.node_group = GenerateGeoNodesGroup(selectObject.name)
        geometryNodeModifier.name = selectObject.name + "GeometryNode"
        bpy.ops.object.modifier_apply(modifier = geometryNodeModifier.name)

        # Add Smooth modifier & apply
        bpy.ops.object.modifier_add(type = 'SMOOTH')
        smoothModifier = extendObject.modifiers[-1]
        smoothModifier.name = 'Smooth'
        smoothModifier.iterations = 20
        bpy.ops.object.modifier_apply(modifier = smoothModifier.name)

        # 恢复选择对象
        bpy.ops.object.select_all(action = 'DESELECT')
        context.view_layer.objects.active = selectObject
        selectObject.select_set(True)

        # 设置法线
        selectObject.data.use_auto_smooth = True
        bpy.ops.object.modifier_add(type = 'DATA_TRANSFER')
        dataTransferModifier = selectObject.modifiers[-1]
        dataTransferModifier.name = 'Data Transfer'
        dataTransferModifier.use_loop_data = True
        dataTransferModifier.data_types_loops = {'CUSTOM_NORMAL'}
        dataTransferModifier.loop_mapping = 'POLYINTERP_NEAREST'
        dataTransferModifier.object = extendObject
        bpy.ops.object.modifier_apply(modifier = dataTransferModifier.name)

        # 删除扩展对象
        bpy.data.objects.remove(extendObject, do_unlink = True)

        return {"FINISHED"}
