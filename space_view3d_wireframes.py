#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "Wireframes",
    "author": "Dalai Felinto",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Shortcut only",
    "description": "Shortcut for wireframes",
    "warning": "",
    "wiki_url": "",
    "category": "Workflow",
    }


import bpy

# ############################################################
# Operator
# ############################################################

class VIEW3D_OT_wireframe_toggle(bpy.types.Operator):
    """Toggle wireframes for the viewport"""
    bl_idname = "view3d.wireframe_toggle"
    bl_label = "Toggle Wireframes"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    @staticmethod
    def _is_wireframe(context):
        space_data = context.space_data
        overlay = space_data.overlay
        shading = space_data.shading

        return overlay.show_wireframes and \
               overlay.show_overlays and \
               shading.show_xray and \
               shading.show_object_outline == False and \
               shading.type in {'SOLID', 'TEXTURE'} and \
               shading.xray_alpha == 0.0

    @staticmethod
    def _push(context):
        space_data = context.space_data
        overlay = space_data.overlay
        shading = space_data.shading

        data_blob = (
            overlay.show_wireframes,
            overlay.show_overlays,
            shading.show_xray,
            shading.type,
            shading.xray_alpha,
            shading.show_object_outline,
            )

        bpy.data_blob = data_blob

    @staticmethod
    def _pop(context):
        space_data = context.space_data
        overlay = space_data.overlay
        shading = space_data.shading

        show_wireframes, show_overlays, show_xray, shading_type, xray_alpha, show_object_outline = bpy.data_blob
        overlay.show_wireframes = show_wireframes
        overlay.show_overlays = show_overlays
        shading.show_xray = show_xray
        shading.type = shading_type
        shading.xray_alpha = xray_alpha
        shading.show_object_outline = show_object_outline

        del bpy.data_blob

    @staticmethod
    def _set_wireframes(context):
        space_data = context.space_data
        overlay = space_data.overlay
        shading = space_data.shading

        overlay.show_wireframes = True
        overlay.show_overlays = True
        shading.show_xray = True
        shading.xray_alpha = 0.0
        shading.show_object_outline = False

        if shading.type not in {'SOLID', 'TEXTURE'}:
            shading.type = 'SOLID'

    @staticmethod
    def _unset_wireframes(context):
        space_data = context.space_data
        overlay = space_data.overlay
        shading = space_data.shading

        overlay.show_wireframes = False
        shading.show_xray = False

    def execute(self, context):
        if self._is_wireframe(context):
            if hasattr(bpy, "data_blob"):
                self._pop(context)
            else:
                self._push(context)
                self._unset_wireframes(context)

        elif hasattr(bpy, "data_blob"):
            self._pop(context)

        else:
            self._push(context)
            self._set_wireframes(context)

        return {'FINISHED'}


# ############################################################
# Un/Register
# ############################################################

classes = (
        VIEW3D_OT_wireframe_toggle,
        )


def register():

    for c in classes:
        bpy.utils.register_class(c)

    """
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.get("3D View")

    if not km:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new('view3d.wireframe_toggle', 'Z', 'PRESS')
    """


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    """
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.get("3D View")

    if km:
        # It shouldn't happen.
        return

    km.keymap_items.remove('view3d.wireframe_toggle', 'Z', 'PRESS')

    if not km.keymap_items:
        kc.keymaps.remove(km)
    """


if __name__ == "__main__":
    register()

