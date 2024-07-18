# -*- coding: utf-8 -*-

import bpy

class BasePanel(object):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80, 0) else 'UI'
    bl_category = '风格化植被'

    @classmethod
    def poll(cls, context):
        return True
