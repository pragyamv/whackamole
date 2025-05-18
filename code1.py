from ursina import*
from ursina.shaders import lit_with_shadows_shader

app=Ursina()
light = DirectionalLight(shadows=True)
light.look_at(Vec3(1, -1, -1))
camera.position = (0, 10, -30)
camera.rotation_x = 20

board = Entity(
    model = load_model('board.glb'),    
    scale=90,
    position=(2, 0, -7),
    cast_shadows=True,
    receive_shadows=True,
    shader=lit_with_shadows_shader
)
mole = Entity(
    model='mole.glb',      
    position=(0, -0.5, 0),
    visible=False
)
hammer = Entity(
    model=load_model('hammer.glb'),   
    scale=3,
    #position = (0, 0, -20),
    cast_shadows=True,
    receive_shadows=True,
    shader=lit_with_shadows_shader
)
hammer_head_offset = Vec3(0, 2, 1)
def update():
    #hammer.x = mouse.x * 20 
    #hammer.y = mouse.y * 10 + 5
    #hammer.z=-10
    hammer.x = clamp(mouse.x * 10, -15, 15) 
    hammer.y = clamp(mouse.y * 10 + 5, 0, 15)
    hammer.z = -12
    targetpos=Vec3(hammer.x, hammer.y, hammer.z)
    hammer.position = targetpos - hammer_head_offset
window.color=color.black
app.run()
