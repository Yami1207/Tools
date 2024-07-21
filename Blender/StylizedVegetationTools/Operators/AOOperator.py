# -*- coding: utf-8 -*-
import bpy
import math
from mathutils import Vector
from StylizedVegetationTools.Operators.Utils import *

class AOOperator(bpy.types.Operator):
    bl_idname = "stylized_vegetation_tools.ao_operator"
    bl_label = 'Bake AO'

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        selectObject = context.view_layer.objects.active
        selectObject.select_set(True)

        # 创建包围盒对象
        volumeObjectName = selectObject.name + "_ExtendMesh"
        volumeObject = self.GenerateVolumeMesh(selectObject, volumeObjectName)

        # 获取射线检查和长度
        raycastDirections = self.GetRaycastDirections()
        raycastLength = max(max(volumeObject.dimensions.x, volumeObject.dimensions.y), volumeObject.dimensions.z)

        # 计算顶点到边界的距离
        vertSignedDistance = []
        verts = [vert.co for vert in selectObject.data.vertices]
        for i in range(len(verts)):
            vertSignedDistance.append(self.GetVertexSDF(volumeObject, verts[i], raycastDirections, raycastLength))

        # 计算顶点AO
        maxDist = max(vertSignedDistance)
        minDist = min(vertSignedDistance)
        invD = 1.0 / (maxDist - minDist)
        for i in range(len(verts)):
            d = (vertSignedDistance[i] - minDist) * invD
            vertSignedDistance[i] = d * d

        # 恢复选择对象
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.context.view_layer.objects.active = selectObject
        selectObject.select_set(True)

        # AO设置到顶点色
        self.SaveAOToVertexColor(selectObject, vertSignedDistance)

        # 删除包围盒对象
        bpy.data.objects.remove(volumeObject, do_unlink = True)

        return {"FINISHED"}
    
    def GetRaycastDirections(self):
        # 创建棱角球顶点作为射线检查的方向
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 2, radius = 1, enter_editmode = False, location = (0, 0, 0))
        sphereObject = bpy.context.object
        sphereObject.name = "RaycastSphere"
        raycastDirections = [vert.co for vert in sphereObject.data.vertices]
        bpy.data.objects.remove(sphereObject, do_unlink = True)
        return raycastDirections

    def GetVertexSDF(self, volumeObject, position, raycastDirections, raycastLength):
        result = 5000
        for dir in raycastDirections:
            success, location, normal, polyIndex = volumeObject.ray_cast(position, dir, distance = raycastLength)
            if success:
                value = math.copysign((location - position).length, -Vector.dot(dir, normal))
                if(abs(value) < abs(result)):
                    result = value
        return result
    
    def GenerateVolumeMesh(self, source, name):
        bpy.ops.object.duplicate(linked=False)
        volumeObject = bpy.context.active_object
        volumeObject.name = name
        volumeObject.select_set(True)

        # 添加Geometry node modifier
        bpy.ops.object.modifier_add(type = 'NODES')
        geometryNodeModifier = volumeObject.modifiers[-1]
        geometryNodeModifier.node_group = GenerateGeoNodesGroup(name)
        geometryNodeModifier.name = name + "GeometryNode"

        # Add Smooth modifier & apply
        bpy.ops.object.modifier_add(type = 'SMOOTH')
        smoothModifier = volumeObject.modifiers[-1]
        smoothModifier.name = 'Smooth'
        smoothModifier.iterations = 20

        # 恢复选择对象
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.context.view_layer.objects.active = source
        source.select_set(True)

        return volumeObject
    
    def SaveAOToVertexColor(self, select, vertSignedDistance):
        mesh = select.data

        # 创建顶点color
        if not mesh.color_attributes:
            mesh.color_attributes.new("Color", 'FLOAT_COLOR', 'POINT')
        
        # 设置顶点颜色
        colorAttr = mesh.attributes.active_color
        if colorAttr.domain == 'CORNER':
            # 在CORNER中，需要遍历面去设置顶点色
            for poly in mesh.polygons:
                for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                    index = mesh.loops[loop_index].vertex_index
                    d = vertSignedDistance[index]
                    colorAttr.data[index].color[0] = d
        else:
            # 直接设置顶点色
            for i in range(len(vertSignedDistance)):
                d = vertSignedDistance[i]
                colorAttr.data[i].color[0] = d
