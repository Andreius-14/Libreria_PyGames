"""
    desconocido -> invoke()      # [❓invoke] Se invoca a una funcion por Delay  

    random.seed(0) -> Inicializa lo random

    🌱 Ursina Tiene shader predeterminado
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

random.seed(0)  # Inicializa lo random
Entity.default_shader = lit_with_shadows_shader  # Definiendo material predeterminado

""" INSTANCIAS """

# 📦 Objeto 3D - Piso
ground = Entity( model="plane", collider="box", scale=64, texture="grass", texture_scale=(4, 4))
editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# 🌱 Instancia Player
# Player - Entidad
player = FirstPersonController( model="cube", z=-10, color=color.orange, origin_y=-0.5, speed=8)
# Player - Propiedad
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))

# 🌱 Instancia Gun
# Arma - Entidad
gun = Entity( model="cube", parent=camera, position=(0.5, -0.25, 0.25), scale=(0.3, 0.2, 1), origin_z=-0.5, color=color.red, on_cooldown=False,)
# Arma - Propiedad Disparo
gun.muzzle_flash = Entity( parent=gun, z=1, world_scale=0.5, model="quad", color=color.yellow, enabled=False)

# 🌱 Instancia Disparo
shootables_parent = Entity()
mouse.traverse_target = shootables_parent


# 📦 Objeto 3D - Pilares
for i in range(4):
    Entity( model="cube", origin_y=-0.5, scale=2, texture="brick", texture_scale=(1, 2), x=random.uniform(-8, 8), z=random.uniform(-8, 8) + 8, collider="box", scale_y=random.uniform(2, 3), color=color.hsv(0, 0, random.uniform(0.9, 1)),)

""" Funciones """
def update():
    if held_keys["left mouse"]:
        shoot()


def shoot():
    # Verificando bool
    if not gun.on_cooldown:
        # print('shoot')
        gun.on_cooldown = True
        # Disparao
        gun.muzzle_flash.enabled = True

        """ Instancias Especiales"""
        from ursina.prefabs.ursfx import ursfx
        # Efecto de Sonido
        ursfx( [(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave="noise", pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0,)
        # Activa Funcion
        invoke(gun.muzzle_flash.disable, delay=0.05)
        invoke(setattr, gun, "on_cooldown", False, delay=0.15)
        # Verificador
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, "hp"):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)


from ursina.prefabs.health_bar import HealthBar


""" ENEMIGO Y ACCION """


class Enemy(Entity):
    # Contructor
    def __init__(self, **kwargs):
        super().__init__( parent=shootables_parent, model="cube", scale_y=2, origin_y=-0.5, color=color.light_gray, collider="box", **kwargs)
        self.health_bar = Entity( parent=self, y=1.2, model="cube", color=color.red, world_scale=(1.5, 0.1, 0.1),)
        self.max_hp = 100
        self.hp = self.max_hp

    # Actualiza por FPS
    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(player.position, "y")
        hit_info = raycast( self.world_position + Vec3(0, 1, 0), self.forward, 30, ignore=(self,))

        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    # Funciones Get y Set
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


# Entidad - Enemy()
enemies = [Enemy(x=x * 4) for x in range(4)]


""" TECLA ESPECIAL """


def pause_input(key):
    if key == "tab":  # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled


# Entidad
pause_handler = Entity(ignore_paused=True, input=pause_input)

# Entidad
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

# Entidad
Sky()


app.run()
