# -*- coding: utf-8 -*-
import bpy

def GenerateGeoNodesGroup(name):
    nodeGroup = bpy.data.node_groups.new(name + '_GeometryNodes', 'GeometryNodeTree')

    # Define interface
    inputSocket = nodeGroup.interface.new_socket(name = "Mesh", description = "Mesh input", in_out = 'INPUT', socket_type = 'NodeSocketGeometry')
    outputSocket = nodeGroup.interface.new_socket(name = "Mesh", description = "Mesh output", in_out = 'OUTPUT', socket_type = 'NodeSocketGeometry')

    # Node Group Input
    inputNode = nodeGroup.nodes.new('NodeGroupInput') 
        
    # Extrude Mesh
    extrudeNode = nodeGroup.nodes.new('GeometryNodeExtrudeMesh')
    extrudeNode.name = "ExtrudeNode"
    extrudeNode.inputs['Offset Scale'].default_value = 1.0
    extrudeNode.inputs['Individual'].default_value = False
    nodeGroup.links.new(inputNode.outputs['Mesh'], extrudeNode.inputs['Mesh'])

    # Mesh To Volume
    meshToVolumeNode = nodeGroup.nodes.new('GeometryNodeMeshToVolume')
    meshToVolumeNode.inputs['Voxel Amount'].default_value = 32
    nodeGroup.links.new(extrudeNode.outputs["Mesh"], meshToVolumeNode.inputs['Mesh'])
    
    # Volume To Mesh
    volumeToMeshNode = nodeGroup.nodes.new('GeometryNodeVolumeToMesh')
    nodeGroup.links.new(meshToVolumeNode.outputs['Volume'], volumeToMeshNode.inputs['Volume'])
    
    # Node Group Output
    outputNode = nodeGroup.nodes.new('NodeGroupOutput')
    nodeGroup.links.new(volumeToMeshNode.outputs['Mesh'], outputNode.inputs['Mesh'])

    return nodeGroup
