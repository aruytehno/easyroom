import bpy
import os
import json
from mathutils import Vector
from datetime import datetime


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def setup_render(config):
    scene = bpy.context.scene
    render = config['render_settings']

    scene.render.engine = render['engine']
    scene.render.resolution_x = render['resolution_x']
    scene.render.resolution_y = render['resolution_y']

    eevee = render['eevee_settings']
    scene.eevee.use_bloom = eevee['use_bloom']
    scene.eevee.bloom_intensity = eevee['bloom_intensity']
    scene.eevee.use_ssr = eevee['use_ssr']
    scene.eevee.use_ssr_refraction = eevee['use_ssr_refraction']
    scene.eevee.use_soft_shadows = eevee['use_soft_shadows']
    scene.eevee.taa_render_samples = eevee['taa_render_samples']
    scene.eevee.taa_samples = eevee['taa_samples']


def create_room(config):
    room = config['room']

    bpy.ops.mesh.primitive_plane_add(size=room['floor']['size'],
                                     location=room['floor']['location'])
    bpy.context.object.name = "Floor"

    for wall in room['walls']:
        bpy.ops.mesh.primitive_plane_add(size=10, location=wall['location'])
        bpy.ops.transform.rotate(value=rad(wall['rotation'][0]), orient_axis='X')
        bpy.ops.transform.rotate(value=rad(wall['rotation'][1]), orient_axis='Y')
        bpy.ops.transform.rotate(value=rad(wall['rotation'][2]), orient_axis='Z')
        bpy.context.object.name = wall['name']


def create_material(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def apply_materials(config):
    room = config['room']
    floor_mat = create_material("Floor_Material", room['floor']['color'], roughness=0.3)
    wall_mat = create_material("Wall_Material", room['wall_color'], roughness=0.5)

    for obj_name, mat in [("Floor", floor_mat), ("Wall_Back", wall_mat), ("Wall_Left", wall_mat)]:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].data.materials.append(mat)


def create_objects(config):
    for obj_data in config['objects']:
        if obj_data['type'] == 'cube':
            bpy.ops.mesh.primitive_cube_add(size=obj_data['size'], location=obj_data['location'])
        elif obj_data['type'] == 'sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=obj_data['radius'], location=obj_data['location'])
        elif obj_data['type'] == 'cylinder':
            bpy.ops.mesh.primitive_cylinder_add(radius=obj_data['radius'], depth=obj_data['depth'],
                                                location=obj_data['location'])

        obj = bpy.context.object
        obj.name = obj_data['name']

        mat = create_material(
            f"{obj_data['name']}_Material",
            obj_data['color'],
            obj_data.get('metallic', 0.0),
            obj_data.get('roughness', 0.5)
        )
        obj.data.materials.append(mat)


def setup_lights(config):
    if "Light" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Light"])

    for light_data in config['lights']:
        bpy.ops.object.light_add(type=light_data['type'], location=light_data['location'])
        light = bpy.context.object
        light.name = light_data['name']
        light.data.energy = light_data['energy']

        if light_data['type'] == 'AREA':
            light.data.size = light_data['size']

        if light_data['type'] == 'SPOT':
            light.data.spot_size = rad(light_data['spot_size'])

        if 'color' in light_data:
            light.data.color = light_data['color'][:3]

        light.rotation_euler = tuple(rad(r) for r in light_data.get('rotation', [0, 0, 0]))


def setup_camera(config):
    if "Camera" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Camera"])

    cam_data = config['camera']
    bpy.ops.object.camera_add(location=cam_data['location'])
    camera = bpy.context.object
    camera.name = "Main_Camera"
    camera.rotation_euler = tuple(rad(r) for r in cam_data['rotation'])
    bpy.context.scene.camera = camera


def rad(degrees):
    return degrees * 3.14159265 / 180


def save_file(extension="blend"):
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scene_{timestamp}.{extension}"
    filepath = os.path.join(out_dir, filename)

    if extension == "blend":
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
    else:
        bpy.context.scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)

    return filepath


def main():
    config = load_config()

    clear_scene()
    setup_render(config)
    create_room(config)
    apply_materials(config)
    create_objects(config)
    setup_lights(config)
    setup_camera(config)

    blend_path = save_file("blend")
    render_path = save_file("png")

    print(f"Blender file: {blend_path}")
    print(f"Render: {render_path}")


if __name__ == "__main__":
    main()