from ursina import *
from ursina.scene import Scene
from ursina.shaders import lit_with_shadows_shader
from random import choice


app = Ursina()
game_active=True
game_font='PixelGame.otf'


#Game Over
def game_over():
    game_over = Text(text='GAME OVER :(', position=(-0.8, 0.1), scale=14, color=rgb(255,0,0),font=game_font)
    global game_active
    game_active=False


#Background
background_texture = load_texture('ArcadeMachines2.jpg')
background = Entity(model='plane',scale=50,position=(0, -5,50),texture=background_texture,shader='flat',collider='mesh')
background.rotation_x=-75
background.scale_x=60


#Camera
camera.position=(-0.3,8,-23)
camera.rotation_x=16


#Entities
hammer=Entity(model='hammer.glb', scale=4, position=(4, 4, -4),cast_shadows=True,receive_shadows=True,shader=lit_with_shadows_shader)
mole1=Entity(model='mole.glb', scale=2.5, position=(-2.4, 1.1, -2),collider='box', enabled=False)
mole2=Entity(model='mole.glb', scale=2.5, position=(-0.5, 1.1, -2),collider='box', enabled=False)
mole3=Entity(model='mole.glb', scale=2.5, position=(2.1, 1.1, -2),collider='box', enabled=False)
mole4=Entity(model='mole.glb', scale=2.5, position=(-3.3, 1.1, -3.5),collider='box', enabled=False)
mole5=Entity(model='mole.glb', scale=2.5, position=(-1.4, 1.1, -3.5),collider='box', enabled=False)
mole6=Entity(model='mole.glb', scale=2.5, position=(0.5, 1.1, -3.4),collider='box', enabled=False)
mole7=Entity(model='mole.glb', scale=2.5, position=(2.3, 1.1, -3.58),collider='box', enabled=False)
board = Entity(model = 'board.glb',scale=80,position=(2, -1, 0),cast_shadows=True,receive_shadows=True,shader=lit_with_shadows_shader,collider='mesh')
moles=[mole1,mole2,mole3,mole4,mole5,mole6,mole7]


#Mole Pop-Up Variables
pop_up_duration = 0.2
pop_down_duration = 0.3
mole_up_y = 1.1
mole_down_y = 0.6 # Adjust this value to hide the mole completely
current_active_mole = None
mole_timer = 0.0
game_elapsed_time=0.0
mole_interval = 1.5 # Time between mole pop-ups


#Hammer Movement and Spawn Mech
hammer_head_offset = Vec3(0.2, 0.7, 1.4)
def update():
    global mole_timer, current_active_mole,game_elapsed_time
    hammer.x = clamp(mouse.x * 5, -10, 10)
    hammer.y = clamp(mouse.y * 5 + 5, 0, 15)
    hammer.z = -12
    targetpos=Vec3(hammer.x, hammer.y, hammer.z)
    hammer.position = targetpos - hammer_head_offset

    mole_timer += time.dt
    game_elapsed_time += time.dt
    mole_interval = max(0.1, 1.0 - (game_elapsed_time // 10) * 0.2)
    if mole_timer >= mole_interval and current_active_mole is None:
        mole_timer = 0.0
        activate_random_mole()
    elif current_active_mole and mole_timer >= pop_up_duration + 1.0: # Keep mole up for 1 second
        mole_timer = 0.0
        deactivate_mole(current_active_mole)


#Up n Down
def activate_random_mole():
    global current_active_mole
    if current_active_mole:
        return
    available_moles = [mole for mole in moles if not mole.enabled]
    if available_moles:
        chosen_mole = choice(available_moles)
        chosen_mole.enabled = True
        chosen_mole.animate_position((chosen_mole.x, mole_up_y, chosen_mole.z), duration=pop_up_duration)
        current_active_mole = chosen_mole

def deactivate_mole(mole_to_deactivate):
    global current_active_mole
    mole_to_deactivate.animate_position((mole_to_deactivate.x, mole_down_y, mole_to_deactivate.z), duration=pop_down_duration)
    invoke(setattr, mole_to_deactivate, 'enabled', False, delay=pop_down_duration)
    current_active_mole = None


#Hammer Animation
def swing_hammer():
    hammer.animate_rotation((90, 0, 0), duration=0.2)
    invoke(setattr, hammer, 'rotation',(0,0,0), delay=0.5)


#Handle Click
def handle_click(hit_mole):
    global current_active_mole
    if hit_mole == current_active_mole:
        clicked()
    swing_hammer()
    deactivate_mole(hit_mole)


#Score
score=0
score_text = Text(text=f'Score : {score}', position=(0.5, 0.45), scale=4,color=rgb(255,174,0  ),font=game_font)
def clicked():
    global game_active
    if game_active is True:
        global score
        score+=1
        score_text.text = f'Score: {score}'

#Lives
lives=3
lives_text = Text(text=f'Lives: {lives}', position=(-0.85, 0.45), scale=4,color=rgb(0,255,0 ),font=game_font)
def fail_click():
    global lives
    if lives > 0:
        lives-=1
        lives_text.text = f'Lives: {lives}'
    if lives == 0:
        game_over()
background.on_click =fail_click
board.on_click =fail_click


#Callers
for mole in moles:
    mole.on_click = Func(handle_click, mole)

for mole in moles:
    mole.y = mole_down_y


app.run()