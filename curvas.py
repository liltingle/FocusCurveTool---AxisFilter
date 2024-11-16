import bpy

bl_info = {
    "name": "Ocultar Canales en el Graph Editor",
    "author": "Mateo",
    "version": (1, 7),
    "blender": (3, 0, 0),
    "location": "Graph Editor > View",
    "description": "Oculta todos los canales excepto el canal seleccionado de las curvas visibles en el Graph Editor. También permite mostrar/ocultar todos los canales, activar solo locaciones o solo rotaciones.",
    "category": "Animation"
}

class ANIM_OT_HideUnselectedChannels(bpy.types.Operator):
    bl_idname = "anim.hide_unselected_channels"
    bl_label = "Activar Curva"
    bl_description = "Activa el canal seleccionado y oculta todos los demás canales en el Graph Editor"
    bl_options = {'REGISTER', 'UNDO'}

    curve_type: bpy.props.EnumProperty(
        items=[
            ('ROT_X', "Rotación X", ""),
            ('ROT_Y', "Rotación Y", ""),
            ('ROT_Z', "Rotación Z", ""),
            ('LOC_X', "Locación X", ""),
            ('LOC_Y', "Locación Y", ""),
            ('LOC_Z', "Locación Z", "")
        ],
        name="Tipo de Canal",
        description="Selecciona el canal que deseas mantener visible",
        default='ROT_Z'
    )

    def execute(self, context):
        obj = context.object
        if not obj or not obj.animation_data or not obj.animation_data.action:
            self.report({'WARNING'}, "Selecciona un objeto con curvas de animación activas.")
            return {'CANCELLED'}

        action = obj.animation_data.action
        fcurves = action.fcurves

        curve_map = {
            'ROT_X': (0, "rotation_euler"),
            'ROT_Y': (1, "rotation_euler"),
            'ROT_Z': (2, "rotation_euler"),
            'LOC_X': (0, "location"),
            'LOC_Y': (1, "location"),
            'LOC_Z': (2, "location"),
        }

        array_index, data_path_part = curve_map[self.curve_type]

        for fcurve in fcurves:
            if data_path_part in fcurve.data_path:
                if fcurve.array_index != array_index:
                    fcurve.hide = True
                else:
                    fcurve.hide = False

        for fcurve in fcurves:
            if not data_path_part in fcurve.data_path:
                fcurve.hide = True

        return {'FINISHED'}

class ANIM_OT_ToggleHideChannels(bpy.types.Operator):
    bl_idname = "anim.toggle_hide_channels"
    bl_label = "Mostrar/Ocultar Todos"
    bl_description = "Muestra o oculta todos los canales de las curvas en el Graph Editor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or not obj.animation_data or not obj.animation_data.action:
            self.report({'WARNING'}, "Selecciona un objeto con curvas de animación activas.")
            return {'CANCELLED'}

        action = obj.animation_data.action
        fcurves = action.fcurves

        hide_all = all(fcurve.hide for fcurve in fcurves)

        for fcurve in fcurves:
            fcurve.hide = not hide_all

        return {'FINISHED'}

class ANIM_OT_ActivateLocationsOnly(bpy.types.Operator):
    bl_idname = "anim.activate_locations_only"
    bl_label = "Activar Solo Locaciones"
    bl_description = "Activa solo los canales de locación (X, Y, Z) y oculta todos los demás canales."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or not obj.animation_data or not obj.animation_data.action:
            self.report({'WARNING'}, "Selecciona un objeto con curvas de animación activas.")
            return {'CANCELLED'}

        action = obj.animation_data.action
        fcurves = action.fcurves

        location_paths = ["location"]
        
        for fcurve in fcurves:
            if any(location in fcurve.data_path for location in location_paths):
                fcurve.hide = False
            else:
                fcurve.hide = True

        return {'FINISHED'}

class ANIM_OT_ActivateRotationsOnly(bpy.types.Operator):
    bl_idname = "anim.activate_rotations_only"
    bl_label = "Activar Solo Rotaciones"
    bl_description = "Activa solo los canales de rotación (X, Y, Z) y oculta todos los demás canales."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or not obj.animation_data or not obj.animation_data.action:
            self.report({'WARNING'}, "Selecciona un objeto con curvas de animación activas.")
            return {'CANCELLED'}

        action = obj.animation_data.action
        fcurves = action.fcurves

        rotation_paths = ["rotation_euler"]
        
        for fcurve in fcurves:
            if any(rotation in fcurve.data_path for rotation in rotation_paths):
                fcurve.hide = False
            else:
                fcurve.hide = True

        return {'FINISHED'}

class GRAPH_PT_hide_unselected_channels(bpy.types.Panel):
    bl_label = "Activar Curva"
    bl_idname = "GRAPH_PT_hide_unselected_channels"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'View'

    def draw(self, context):
        layout = self.layout
        layout.operator(ANIM_OT_ToggleHideChannels.bl_idname, text="Mostrar/Ocultar Todos")
        
        # Sección de locaciones
        box = layout.box()
        box.label(text="Locaciones")
        box.operator("anim.hide_unselected_channels", text="Locación X", icon='MESH_PLANE').curve_type = 'LOC_X'
        box.operator("anim.hide_unselected_channels", text="Locación Y", icon='MESH_PLANE').curve_type = 'LOC_Y'
        box.operator("anim.hide_unselected_channels", text="Locación Z", icon='MESH_PLANE').curve_type = 'LOC_Z'
        
        # Sección de rotaciones
        box = layout.box()
        box.label(text="Rotaciones")
        box.operator("anim.hide_unselected_channels", text="Rotación X", icon='MESH_CIRCLE').curve_type = 'ROT_X'
        box.operator("anim.hide_unselected_channels", text="Rotación Y", icon='MESH_CIRCLE').curve_type = 'ROT_Y'
        box.operator("anim.hide_unselected_channels", text="Rotación Z", icon='MESH_CIRCLE').curve_type = 'ROT_Z'
        
        layout.operator(ANIM_OT_ActivateLocationsOnly.bl_idname, text="Solo Locaciones")
        layout.operator(ANIM_OT_ActivateRotationsOnly.bl_idname, text="Solo Rotaciones")


def register():
    bpy.utils.register_class(ANIM_OT_HideUnselectedChannels)
    bpy.utils.register_class(ANIM_OT_ToggleHideChannels)
    bpy.utils.register_class(ANIM_OT_ActivateLocationsOnly)
    bpy.utils.register_class(ANIM_OT_ActivateRotationsOnly)
    bpy.utils.register_class(GRAPH_PT_hide_unselected_channels)

def unregister():
    bpy.utils.unregister_class(ANIM_OT_HideUnselectedChannels)
    bpy.utils.unregister_class(ANIM_OT_ToggleHideChannels)
    bpy.utils.unregister_class(ANIM_OT_ActivateLocationsOnly)
    bpy.utils.unregister_class(ANIM_OT_ActivateRotationsOnly)
    bpy.utils.unregister_class(GRAPH_PT_hide_unselected_channels)

if __name__ == "__main__":
    register()
