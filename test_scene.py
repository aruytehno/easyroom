import bpy
import os
import math
from mathutils import Vector


# Очистка сцены
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


# Настройка рендера на Eevee
def setup_eevee_render():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'

    # Настройки Eevee
    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.05
    scene.eevee.use_ssr = True  # Screen Space Reflections
    scene.eevee.use_ssr_refraction = True
    scene.eevee.use_soft_shadows = True

    # Для ноутбука - уменьшаем качество для скорости
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100

    # Anti-aliasing
    scene.eevee.taa_render_samples = 32
    scene.eevee.taa_samples = 16


# Создание простой комнаты
def create_room():
    # Создаем плоскость как пол
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"

    # Создаем стены
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, -5, 5))
    bpy.ops.transform.rotate(value=math.radians(90), orient_axis='X')
    wall_back = bpy.context.object
    wall_back.name = "Wall_Back"

    bpy.ops.mesh.primitive_plane_add(size=10, location=(-5, 0, 5))
    bpy.ops.transform.rotate(value=math.radians(90), orient_axis='Y')
    wall_left = bpy.context.object
    wall_left.name = "Wall_Left"


# Создание материалов
def create_materials():
    # Материал для пола
    mat_floor = bpy.data.materials.new(name="Floor_Material")
    mat_floor.use_nodes = True
    nodes = mat_floor.node_tree.nodes
    nodes.clear()

    # Создаем простую нод-структуру
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.8, 0.7, 0.6, 1)  # Светлое дерево
    bsdf.inputs['Roughness'].default_value = 0.3

    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Соединяем ноды
    links = mat_floor.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Применяем материал к полу
    if "Floor" in bpy.data.objects:
        bpy.data.objects["Floor"].data.materials.append(mat_floor)

    # Материал для стен
    mat_wall = bpy.data.materials.new(name="Wall_Material")
    mat_wall.use_nodes = True
    nodes = mat_wall.node_tree.nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)  # Белый
    bsdf.inputs['Roughness'].default_value = 0.5

    output = nodes.new(type='ShaderNodeOutputMaterial')

    links = mat_wall.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Применяем к стенам
    for obj_name in ["Wall_Back", "Wall_Left"]:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].data.materials.append(mat_wall)


# Создание объектов
def create_objects():
    # Простой куб
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    cube = bpy.context.object
    cube.name = "Main_Cube"

    # Сфера
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3, 0, 1))
    sphere = bpy.context.object
    sphere.name = "Sphere"

    # Цилиндр
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.8, depth=2, location=(-3, 0, 1))
    cylinder = bpy.context.object
    cylinder.name = "Cylinder"

    # Материалы для объектов
    create_object_materials()


def create_object_materials():
    # Красный материал для куба
    mat_red = bpy.data.materials.new(name="Red_Material")
    mat_red.use_nodes = True
    nodes = mat_red.node_tree.nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (1, 0.2, 0.2, 1)
    bsdf.inputs['Metallic'].default_value = 0.2
    bsdf.inputs['Roughness'].default_value = 0.1

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links = mat_red.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Синий материал для сферы
    mat_blue = bpy.data.materials.new(name="Blue_Material")
    mat_blue.use_nodes = True
    nodes = mat_blue.node_tree.nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.2, 0.4, 1, 1)
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.05

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links = mat_blue.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Зеленый материал для цилиндра
    mat_green = bpy.data.materials.new(name="Green_Material")
    mat_green.use_nodes = True
    nodes = mat_green.node_tree.nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.2, 0.8, 0.3, 1)
    bsdf.inputs['Roughness'].default_value = 0.3

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links = mat_green.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Применяем материалы
    if "Main_Cube" in bpy.data.objects:
        bpy.data.objects["Main_Cube"].data.materials.append(mat_red)
    if "Sphere" in bpy.data.objects:
        bpy.data.objects["Sphere"].data.materials.append(mat_blue)
    if "Cylinder" in bpy.data.objects:
        bpy.data.objects["Cylinder"].data.materials.append(mat_green)


# Настройка освещения
def setup_lighting():
    # Удаляем стандартный свет
    if "Light" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)

    # Создаем основное освещение (Area light)
    bpy.ops.object.light_add(type='AREA', location=(4, 4, 8))
    area_light = bpy.context.object
    area_light.name = "Main_Area_Light"
    area_light.data.energy = 300
    area_light.data.size = 4
    area_light.rotation_euler = (math.radians(45), 0, math.radians(-45))

    # Создаем заполняющий свет
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    fill_light = bpy.context.object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 100
    fill_light.data.size = 3
    fill_light.data.color = (0.9, 0.95, 1.0)  # Холодный свет

    # Создаем задний свет
    bpy.ops.object.light_add(type='SPOT', location=(0, 5, 5))
    back_light = bpy.context.object
    back_light.name = "Back_Light"
    back_light.data.energy = 150
    back_light.data.spot_size = math.radians(45)
    back_light.rotation_euler = (math.radians(90), 0, 0)


# Настройка камеры
def setup_camera():
    # Удаляем стандартную камеру
    if "Camera" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Camera"], do_unlink=True)

    # Создаем новую камеру
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.object
    camera.name = "Main_Camera"

    # Направляем камеру на сцену
    camera.rotation_euler = (
        math.radians(60),  # Pitch
        0,  # Yaw
        math.radians(45)  # Roll
    )

    # Устанавливаем активной камерой
    bpy.context.scene.camera = camera


# Сохранение файла
def save_blend_file(filepath):
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"Файл сохранен: {filepath}")


# Рендеринг изображения
def render_image(filepath):
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"Изображение сохранено: {filepath}")


# Основная функция
def main():
    print("=" * 50)
    print("Создание тестовой сцены для Blender + Eevee")
    print("=" * 50)

    # Очистка сцены
    clear_scene()

    # Настройка рендера
    setup_eevee_render()

    # Создание объектов
    create_room()
    create_materials()
    create_objects()

    # Настройка освещения и камеры
    setup_lighting()
    setup_camera()

    # Пути для сохранения
    blend_path = r"C:\Users\simbiom\PycharmProjects\easyroom\test_scene.blend"
    render_path = r"C:\Users\simbiom\PycharmProjects\easyroom\render_output.png"

    # Сохранение файла Blender
    save_blend_file(blend_path)

    # Рендеринг изображения
    render_image(render_path)

    print("\nГотово! Сцена создана и отрендерена.")
    print(f"Файл Blender: {blend_path}")
    print(f"Изображение: {render_path}")


# Запуск скрипта
if __name__ == "__main__":
    main()