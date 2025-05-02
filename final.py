from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Camera-related variables
camera_pos = (0,500,500)
thrid_person_camera_pos = (0,-500,500)
camera_change_rate = 5

fovY = 120  # Field of view
GRID_LENGTH = 92  # Length of grid lines
rand_var = 423
first_person = False

active_indicators = []  
left_indicator = False
right_indicator = False

game_over = False
player_life = 5
game_score = 0

switch_message = ""  
message_timer = 0 

class Player:
    global_x = 0
    global_y = 0
    global_z = 0
    global_angle = 0
    rotatex = 0
    angle_rad = math.radians(global_angle)
    movement = True
    cam_x = global_x 
    cam_y = global_y 
    cam_z = 100
    costume_no = 0
    costumes = [(54/255, 34/255, 4/255), (1, 0, 0), (1/255, 50/255, 32/255)]
    center_x = cam_x - math.sin(angle_rad) * 100  
    center_y = cam_y + math.cos(angle_rad) * 100  
    center_z = cam_z  
    def __init__(self):
         self.xposition = 0
         self.yposition = 0
    def draw_player(self):
        glPushMatrix()
        #For movement
        glTranslatef(self.global_x, self.global_y, 0) 
        glRotatef(self.global_angle, 0, 0, 1)
        glRotatef(self.rotatex, 1, 0, 0)
        #Drawing the cube
        r,g,b = Player.costumes[Player.costume_no]
        glColor3f(r,g,b)
        glTranslatef(self.xposition, self.yposition, 40)  #x,y,z
        glutSolidCube(60)
        #Drawing the legs
        glColor3f(0, 0, 0)
        glTranslatef(self.xposition+20, 0, -40) 
        gluCylinder(gluNewQuadric(), 5, 10, 40, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        glTranslatef(self.xposition-40, 0, 0) 
        gluCylinder(gluNewQuadric(), 5, 10, 40, 10, 10)
        #Drawing the right hand
        glColor3f(1, 0.9, 0.7)
        glTranslatef(self.xposition+40, 0, 70) 
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 70, 10, 10)
        #Drawing the sword
        Sword.draw_sword(70)
        #Drawing the left hand
        glColor3f(1, 0.9, 0.7)
        glTranslatef(self.xposition-40, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 70, 10, 10)
        #Drawing the head
        glColor3f(0, 0, 0)
        glRotatef(90, 1, 0, 0)
        glTranslatef(self.xposition+20, 0, 20)
        gluSphere(gluNewQuadric(), 15, 10, 10)
        glPopMatrix()



class Sword:
    angle = 90
    swinging_down = False  
    returning = False  
    types_and_strengths = {"Type 1":[50,True], "Type 2": [100,False], "Type 3": [500,True]}
    sword_colors = {"Type 1": (128/255, 128/255, 128/255), "Type 2": (0.8, 0.8, 0), "Type 3": (1, 0, 0)}
    unlocked_weapons = {"Type 1": True, "Type 2": False, "Type 3": False}
    current_type = "Type 1"
    current_color = sword_colors[current_type]
    def __init__(self):
        self.current_strength = Sword.types_and_strengths[self.current_type][0]
        

    @staticmethod
    def unlock_weapons(score):
        if score >= 100:
            Sword.unlocked_weapons["Type 2"] = True
        if score >= 500:
            Sword.unlocked_weapons["Type 3"] = True

    @staticmethod
    def switch_weapon():
        global switch_message, message_timer
        weapon_types = list(Sword.types_and_strengths.keys())
        current_index = weapon_types.index(Sword.current_type)
        for i in range(1, len(weapon_types)):
            next_index = (current_index + i) % len(weapon_types)
            next_weapon = weapon_types[next_index]
            if Sword.unlocked_weapons[next_weapon]:
                Sword.current_type = next_weapon
                Sword.update_weapon_properties()
                switch_message = f"Switched to {next_weapon}"  
                message_timer = 3  
                return switch_message
        switch_message = "Weapon is locked!"  
        message_timer = 3  
        return switch_message

    @staticmethod
    def update_weapon_properties():
        Sword.current_strength = Sword.types_and_strengths[Sword.current_type][0]
        Sword.current_color = Sword.sword_colors[Sword.current_type]
    
    @staticmethod
    def draw_sword(z):
        glPushMatrix()
        glTranslatef(0, 0, z)  
        glRotatef(Sword.angle, 1, 0, 0)
        glColor3f(0.5, 0.2, 0.1)  # Sword handle color (brown)
        gluCylinder(gluNewQuadric(), 3, 3, 10, 10, 10)  # Sword handle
        glTranslatef(0, 0, 10) 
        r, g, b = Sword.current_color
        glColor3f(r,g,b)  # Sword blade color (gray)
        gluCylinder(gluNewQuadric(), 2, 2, 50, 10, 10)  # Sword blade
        glPopMatrix()


class Fruit:
    fruits = [
        {"shape": "sphere", "color": (1, 0, 0), "hardness": 1, "points": 10},
        {"shape": "sphere", "color": (0, 1, 0), "hardness": 2, "points": 20},
        {"shape": "sphere", "color": (1, 1, 0), "hardness": 3, "points": 30},
        {"shape": "cube", "color": (1, 0.5, 0), "hardness": 4, "points": 40},
        {"shape": "bomb", "color": (0, 0, 0), "hardness": 10, "points": -1}
    ]
    
    active_fruits = []
    max_fruits = 4
    can_spawn = True
    sword_range = 120
    player_radius = 40

    @staticmethod
    def spawn_fruit():
        if len(Fruit.active_fruits) < Fruit.max_fruits and Fruit.can_spawn == True:
            valid_position = False
            attempts = 0
            
            while valid_position == False and attempts < 10:
                attempts += 1
                
                angle_offset = random.choice([0, math.pi/2, -math.pi/2, math.pi/4, -math.pi/4])
                
                distance = random.uniform(Fruit.player_radius + 30, Fruit.sword_range)
                
                x = Player.global_x - math.sin(Player.angle_rad + angle_offset) * distance
                y = Player.global_y + math.cos(Player.angle_rad + angle_offset) * distance
                z = -50
                
                dist_to_player = math.sqrt((x - Player.global_x)**2 + (y - Player.global_y)**2)
                if dist_to_player > Fruit.player_radius + 20:
                    valid_position = True
            
            if valid_position == False:
                return
                
            vz = random.uniform(3, 5)
            peak_z = random.uniform(150, 250)
                
            if random.random() < 0.15:
                fruit_type = 4
            else:
                fruit_type = random.randint(0, 3)
            
            fruit_id = random.randint(0, 1000000)
            dx = x - Player.global_x
            dy = y - Player.global_y
            angle = math.atan2(dy, dx) - Player.angle_rad
            angle = (angle + math.pi) % (2 * math.pi) - math.pi
            side = "left" if angle > 0 else "right"
            global active_indicators
            active_indicators.append((side, fruit_id))



            Fruit.active_fruits.append({
                "type": fruit_type,
                "x": x,
                "y": y,
                "z": z,
                "vx": 0,
                "vy": 0,
                "vz": vz,
                "peak_z": peak_z,
                "rising": True,
                "sliced": False,
                "slice_time": 0,
                "halves": []
            })
            Fruit.can_spawn = False
    
    @staticmethod
    def update_fruits(delta_time):
        global left_indicator, right_indicator
        left_fruits = False
        right_fruits = False
        
        for fruit in Fruit.active_fruits[:]:
            dx = fruit["x"] - Player.global_x
            dy = fruit["y"] - Player.global_y
            angle = math.atan2(dy, dx) - Player.angle_rad
            angle = (angle + math.pi) % (2 * math.pi) - math.pi
            if angle > 0:
                left_fruits = True
            else:
                right_fruits = True
            
            if fruit["sliced"] == False:
                if fruit["rising"] == True:
                    fruit["z"] += fruit["vz"] * delta_time * 5
                    if fruit["z"] >= fruit["peak_z"]:
                        fruit["rising"] = False
                        fruit["vz"] *= -1
                else:
                    fruit["z"] += fruit["vz"] * delta_time * 5
                    
                if fruit["z"] < -60:
                    Fruit.active_fruits.remove(fruit)
                    Fruit.can_spawn = True
                    if fruit["type"] != 4:
                        global player_life
                        player_life -= 1
            else:
                fruit["slice_time"] += delta_time
                if fruit["slice_time"] > 1.5:
                    Fruit.active_fruits.remove(fruit)
                    Fruit.can_spawn = True
                    continue
                
                for half in fruit["halves"]:
                    half["x"] += half["vx"] * delta_time * 5
                    half["y"] += half["vy"] * delta_time * 5
                    half["z"] += half["vz"] * delta_time * 5
        left_indicator = left_fruits
        right_indicator = right_fruits
        
        Fruit.spawn_fruit()

    @staticmethod
    def check_sword_collision():
        global game_score, player_life, game_over
        if (Sword.swinging_down == False and Sword.returning == False):
            return
        sword_length = Fruit.sword_range
        sword_width = 25
        sword_start = [Player.global_x,Player.global_y,Player.global_z + 100]
        
        sword_angle_rad = math.radians(Sword.angle)
        sword_end = [
            sword_start[0] - math.sin(Player.angle_rad) * sword_length * math.cos(sword_angle_rad),
            sword_start[1] + math.cos(Player.angle_rad) * sword_length * math.cos(sword_angle_rad),
            sword_start[2] + sword_length * math.sin(sword_angle_rad)
        ]
        if not hasattr(Fruit, 'prev_sword_end'):
            Fruit.prev_sword_end = sword_end
        sword_movement = [
            sword_end[0] - Fruit.prev_sword_end[0],
            sword_end[1] - Fruit.prev_sword_end[1],
            sword_end[2] - Fruit.prev_sword_end[2]
        ]
        for fruit in Fruit.active_fruits[:]:
            if fruit["sliced"] == True:
                continue
            fruit_pos = [fruit["x"], fruit["y"], fruit["z"]]
            fruit_radius = 20
            sword_vec = [sword_end[0]-sword_start[0], sword_end[1]-sword_start[1], sword_end[2]-sword_start[2]]
            fruit_vec = [fruit_pos[0]-sword_start[0], fruit_pos[1]-sword_start[1], fruit_pos[2]-sword_start[2]]
            
            dot = 0
            for i in range(3):
                dot += sword_vec[i]*fruit_vec[i]
            sword_len_sq = 0
            for i in range(3):
                sword_len_sq += sword_vec[i]**2
            t = max(0, min(1, dot/sword_len_sq))
            
            closest_point = [
                sword_start[0] + t*sword_vec[0],
                sword_start[1] + t*sword_vec[1],
                sword_start[2] + t*sword_vec[2]
            ]
            
            distance = 0
            for i in range(3):
                distance += (fruit_pos[i]-closest_point[i])**2
            distance = math.sqrt(distance)
            movement_len = 0
            for i in range(3):
                movement_len += sword_movement[i]**2
            movement_len = math.sqrt(movement_len)
            if movement_len > 0:
                movement_dir = []
                for i in range(3):
                    movement_dir.append(sword_movement[i]/movement_len)
                movement_dot = 0
                for i in range(3):
                    movement_dot += movement_dir[i]*(fruit_pos[i]-Fruit.prev_sword_end[i])
                closest_dist_sq = 0
                for i in range(3):
                    closest_dist_sq += (fruit_pos[i] - (Fruit.prev_sword_end[i] + movement_dir[i]*movement_dot))**2
                if distance < (fruit_radius + sword_width) or closest_dist_sq < (fruit_radius + sword_width)**2:
                    fruit["sliced"] = True
                    slice_dir = []
                    for i in range(3):
                        if movement_len > 0:
                            slice_dir.append(sword_movement[i])
                        else:
                            slice_dir.append(random.uniform(-1, 1))
                    slice_dir_len = 0
                    for i in range(3):
                        slice_dir_len += slice_dir[i]**2
                    slice_dir_len = math.sqrt(slice_dir_len)
                    if slice_dir_len > 0:
                        temp = []
                        for i in range(3):
                            temp.append(slice_dir[i]/slice_dir_len)
                        slice_dir = temp
                    fruit["halves"] = [
                        {
                            "x": fruit["x"],
                            "y": fruit["y"],
                            "z": fruit["z"],
                            "vx": slice_dir[0] * 8 + random.uniform(-2, 2),
                            "vy": slice_dir[1] * 8 + random.uniform(-2, 2),
                            "vz": slice_dir[2] * 8 + random.uniform(2, 5)
                        },
                        {
                            "x": fruit["x"],
                            "y": fruit["y"],
                            "z": fruit["z"],
                            "vx": -slice_dir[0] * 8 + random.uniform(-2, 2),
                            "vy": -slice_dir[1] * 8 + random.uniform(-2, 2),
                            "vz": -slice_dir[2] * 4 + random.uniform(2, 5)
                        }
                    ]
                    
                    if fruit["type"] == 4:
                        player_life -= 1
                        if player_life <= 0:
                            game_over = True
                    else:
                        game_score += Fruit.fruits[fruit["type"]]["points"]
        Fruit.prev_sword_end = sword_end

    @staticmethod
    def draw_fruits():
        for fruit in Fruit.active_fruits:
            if fruit["sliced"] == False:
                glPushMatrix()
                glTranslatef(fruit["x"], fruit["y"], fruit["z"])
                fruit_type = Fruit.fruits[fruit["type"]]
                glColor3f(*fruit_type["color"])
                
                if fruit_type["shape"] == "sphere":
                    glutSolidSphere(20, 10, 10)
                elif fruit_type["shape"] == "cube":
                    glutSolidCube(35)
                elif fruit_type["shape"] == "bomb":
                    glutSolidSphere(22, 10, 10)
                    glColor3f(0.5, 0.5, 0.5)
                    glTranslatef(0, 0, 22)
                    glutSolidCone(6, 12, 10, 10)
                glPopMatrix()
            else:
                for i, half in enumerate(fruit["halves"]):
                    glPushMatrix()
                    glTranslatef(half["x"], half["y"], half["z"])
                    fruit_type = Fruit.fruits[fruit["type"]]
                    glColor3f(*fruit_type["color"])
                    
                    if fruit_type["shape"] == "sphere":
                        glutSolidSphere(12, 10, 10)
                    elif fruit_type["shape"] == "cube":
                        glutSolidCube(20)
                    elif fruit_type["shape"] == "bomb":
                        glutSolidSphere(15, 10, 10)
                        glColor3f(0.5, 0.5, 0.5)
                        glTranslatef(0, 0, 15)
                        glutSolidCone(4, 8, 10, 10)
                    glPopMatrix()

def draw_indicators():
    if left_indicator == True or right_indicator == True:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        if left_indicator == True:
            glColor3f(1, 0.2, 0.2)
            glBegin(GL_TRIANGLES)
            glVertex2f(50, 400)
            glVertex2f(100, 370)
            glVertex2f(100, 430)
            glEnd()
            pulse = abs(math.sin(time.time() * 3)) * 0.3 + 0.7
            glColor3f(1, pulse, pulse)
            glBegin(GL_TRIANGLES)
            glVertex2f(60, 400)
            glVertex2f(90, 380)
            glVertex2f(90, 420)
            glEnd()
        
        if right_indicator == True:
            glColor3f(1, 0.2, 0.2)
            glBegin(GL_TRIANGLES)
            glVertex2f(950, 400)
            glVertex2f(900, 370)
            glVertex2f(900, 430)
            glEnd()
            pulse = abs(math.sin(time.time() * 3)) * 0.3 + 0.7
            glColor3f(1, pulse, pulse)
            glBegin(GL_TRIANGLES)
            glVertex2f(940, 400)
            glVertex2f(910, 380)
            glVertex2f(910, 420)
            glEnd()
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def player_lie_down():
    Player.rotatex = 90


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global game_score, first_person, camera_pos, thrid_person_camera_pos, camera_change_rate
    
    # Rotate gun left (A key)
    if key == b'a':
        Player.global_angle+=20
        Player.angle_rad = math.radians(Player.global_angle)
        Player.cam_x = Player.global_x 
        if (Player.global_angle%360 >= 90 and Player.global_angle%360 <= 270) or (Player.global_angle%360 >= -90 and Player.global_angle%360 <= -270):
            Player.cam_y = Player.global_y - 20
        else:
            Player.cam_y = Player.global_y + 20

        Player.center_x = Player.cam_x - math.sin(Player.angle_rad) * 100  
        Player.center_y = Player.cam_y + math.cos(Player.angle_rad) * 100  
        Player.center_z = Player.cam_z  
    # Rotate gun right (D key)
    if key == b'd':
        Player.global_angle-=20
        Player.angle_rad = math.radians(Player.global_angle)
        Player.cam_x = Player.global_x
        if (Player.global_angle%360 >= 90 and Player.global_angle%360 <= 270) or (Player.global_angle%360 >= -90 and Player.global_angle%360 <= -270):
            Player.cam_y = Player.global_y - 20
        else:
            Player.cam_y = Player.global_y + 20 

        Player.center_x = Player.cam_x - math.sin(Player.angle_rad) * 100  
        Player.center_y = Player.cam_y + math.cos(Player.angle_rad) * 100  
        Player.center_z = Player.cam_z  

    #To change costumes
    if key == b'c':
        Player.costume_no = (Player.costume_no+1)%3
    
    #To change sword types
    if key == b'e':
        message = Sword.switch_weapon()
        if "locked" in message:
            draw_text(400, 400, message, GLUT_BITMAP_HELVETICA_18)
        else:
            print(message)  
    if not first_person:
        x, y, z = thrid_person_camera_pos

        # moving camera front
        if key == b'k':
            if not first_person:
                y += camera_change_rate

        # moving camera back
        if key == b'l':
            if not first_person:
                y -= camera_change_rate

        thrid_person_camera_pos = (x, y, z)
        camera_pos = thrid_person_camera_pos


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    
    global camera_pos, thrid_person_camera_pos
    
    x, y, z = camera_pos
    
    if not first_person:
        x, y, z = thrid_person_camera_pos
    
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
         z += camera_change_rate

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= camera_change_rate
    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= camera_change_rate  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += camera_change_rate # Small angle increment for smooth movement

    if not first_person:
        thrid_person_camera_pos = (x, y, z)
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    global first_person
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not Sword.swinging_down and not Sword.returning:
            Sword.swinging_down = True  


def setupCamera():
    global first_person, thrid_person_camera_pos
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    if first_person:

        Player.cam_z = Player.global_z + 100
    
        Player.center_x = Player.cam_x - math.sin(Player.angle_rad) * 100  
        Player.center_y = Player.cam_y + math.cos(Player.angle_rad) * 100  
        Player.center_z = Player.cam_z  

        gluLookAt(Player.cam_x, Player.cam_y, Player.cam_z,
                  Player.center_x, Player.center_y, Player.center_z,
                  0, 0, 1)  # The up-vector (positive Z-axis) is aligned with the world up
    else:
        # Extract camera position and look-at target
        x, y, z = thrid_person_camera_pos
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)


def idle():
    global game_score
    Sword.unlock_weapons(game_score)
    
    if Sword.swinging_down:
        time.sleep(0.01)  
        Sword.angle -= 5  
        if Sword.angle <= 0:  
            Sword.swinging_down = False
            Sword.returning = True  
    elif Sword.returning:
        time.sleep(0.01)  
        Sword.angle += 5  
        if Sword.angle >= 90:  
            Sword.returning = False
    glutPostRedisplay()


def draw_grid():
    global GRID_LENGTH
    y = -600
    x = 600
    count = 0
    for j in range(1,14):
        for i in range(1,14):
            if i%13 == 0:
                if count%2 == 0:
                        glBegin(GL_QUAD_STRIP)
                        glColor3f(1, 1, 1)
                        glVertex3f(x, y, 0)
                        glVertex3f(x, y+GRID_LENGTH, 0)
                        glVertex3f(x-GRID_LENGTH, y, 0)
                        glVertex3f(x-GRID_LENGTH, y+GRID_LENGTH, 0)
                        glEnd()
                else:
                        glBegin(GL_QUAD_STRIP)
                        glColor3f(0.7, 0.5, 0.95)
                        glVertex3f(x, y, 0)
                        glVertex3f(x, y+GRID_LENGTH, 0)
                        glVertex3f(x-GRID_LENGTH, y, 0)
                        glVertex3f(x-GRID_LENGTH, y+GRID_LENGTH, 0)
                        glEnd()
                x = 600
                y += GRID_LENGTH
                count+=1
            else:
                if count%2 == 0:
                        glBegin(GL_QUAD_STRIP)
                        glColor3f(1, 1, 1)
                        glVertex3f(x, y, 0)
                        glVertex3f(x, y+GRID_LENGTH, 0)
                        glVertex3f(x-GRID_LENGTH, y, 0)
                        glVertex3f(x-GRID_LENGTH, y+GRID_LENGTH, 0)
                        glEnd()
                else:
                        glBegin(GL_QUAD_STRIP)
                        glColor3f(0.7, 0.5, 0.95)
                        glVertex3f(x, y, 0)
                        glVertex3f(x, y+GRID_LENGTH, 0)
                        glVertex3f(x-GRID_LENGTH, y, 0)
                        glVertex3f(x-GRID_LENGTH, y+GRID_LENGTH, 0)
                        glEnd()
                x-=GRID_LENGTH
                count+=1
        
def draw_walls():
    glBegin(GL_QUAD_STRIP)
    glColor3f(0, 0, 1)
    glVertex3f(600, -600, 0)
    glVertex3f(600, -600, 100)
    glVertex3f(600, 596, 0)
    glVertex3f(600, 596, 100)
    glEnd()

    glBegin(GL_QUAD_STRIP)
    glColor3f(0.5, 1, 1)
    glVertex3f(600, -600, 0)
    glVertex3f(600, -600, 100)
    glVertex3f(-596, -600, 0)
    glVertex3f(-596, -600, 100)
    glEnd()

    glBegin(GL_QUAD_STRIP)
    glColor3f(0, 1, 0)
    glVertex3f(-596, -600, 0)
    glVertex3f(-596, -600, 100)
    glVertex3f(-596, 596, 0)
    glVertex3f(-596, 596, 100)
    glEnd()

    glBegin(GL_QUAD_STRIP)
    glColor3f(1, 1, 1)
    glVertex3f(-596, 596, 0)
    glVertex3f(-596, 596, 100)
    glVertex3f(600, 596, 0)
    glVertex3f(600, 596, 100)
    glEnd()

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    global message_timer,switch_message
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    draw_grid()
    draw_walls()
    player = Player()
    player.draw_player()

    # Update and draw fruits
    Fruit.update_fruits(0.016)
    Fruit.check_sword_collision()
    Fruit.draw_fruits()
    
    # Draw score and lives
    draw_text(50, 750, f"Score: {game_score}")
    draw_text(50, 720, f"Lives: {player_life}")

    # Display the sword switch message
    if message_timer > 0:
        draw_text(400, 400, switch_message, GLUT_BITMAP_HELVETICA_18)
        message_timer -= 0.016  # Decrease the timer (assuming 60 FPS)

    if game_over:
        draw_text(400, 400, "GAME OVER", GLUT_BITMAP_HELVETICA_12)
    draw_indicators()
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D Ninja Turtle")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle) 

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()