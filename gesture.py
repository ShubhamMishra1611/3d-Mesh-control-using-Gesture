bl_info = {
    "name": "Gesture Mesh control",
    "author": "Shubham Mishra",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add",
    "description": "Controls mesh using hand gesture in real time",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy
from bpy.types import (Panel,Operator)
import cv2
import numpy as np
import hand_track as ht
import pickle

path = "DTC.pkl"   # Enter your path for DTC.pkl here
model = pickle.load(open(path,"rb"))

obj = None

def get_action(coordinates,skip_factor=5,landmarks = None):
    global obj
    if len(coordinates) < 5:
        return None
    
    # calculate area for each element in coordinates
    areas = []
    for coordinate in coordinates:
        area = 0
        j=len(coordinate)-1
        for i in range(len(coordinate)):
            area += (coordinate[j][0]+coordinate[i][0])*(coordinate[j][1]-coordinate[i][1])
            j=i
        areas.append(abs(area)/2)
    
    # check if the area is increasing or decreasing
    inc = 0
    for i in range(len(areas)-1):
        if areas[i+1] > areas[i]:
            inc += 1
        else:
            inc -= 1

    if inc > 3:
        obj.scale[0]+=0.1
        obj.scale[1]+=0.1
        obj.scale[2]+=0.1
        bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP",iterations = 1)
    elif inc < -3:
        obj.scale[0]-=0.1
        obj.scale[1]-=0.1
        obj.scale[2]-=0.1
        bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP",iterations = 1)
    else:
        pass

    
    axis = None
    landmarks = landmarks[:,1:]
    landmark_mean_x = np.mean(landmarks[:,0])
    landmark_mean_y = np.mean(landmarks[:,1])
    normalized_landmarks = (landmarks - np.array([landmark_mean_x,landmark_mean_y]))/np.max(np.abs([landmarks[:,0],landmarks[:,1]]),axis=1)
    axis = int(model.predict([normalized_landmarks.flatten()]))
    axis_s = {0:"X",1:"Y",2:"Z"}
    req_coordinates = coordinates[::skip_factor]
    angles = []
    for coor in range(len(req_coordinates)-1):
        for i in range(len(req_coordinates[coor])):
            m1 = req_coordinates[coor][i][1]/req_coordinates[coor][i][0]
            m2 = req_coordinates[coor+1][i][1]/req_coordinates[coor+1][i][0]
            angle = np.arctan((m2-m1)/(1+m1*m2))
            angles.append(angle)
    mean_angle = np.mean(angles)
    print(f'{mean_angle=}')
    if mean_angle > 0.1:
        bpy.ops.transform.rotate(value = mean_angle, orient_axis = axis_s[axis],orient_type = 'GLOBAL')
        bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP",iterations = 1)
    elif mean_angle < -0.1:
        bpy.ops.transform.rotate(value = mean_angle, orient_axis = axis_s[axis],orient_type = 'GLOBAL')
        bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP",iterations = 1)
    else:
        pass


class ButtonOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "random.1"
    bl_label = "Simple Random Operator"

    

    def execute(self, context):
        global obj
        obj = bpy.context.active_object
        cap = cv2.VideoCapture(0)
        detector = ht.TrackHand()
        coordinates = []
        for i in range(1000):
            ret,img = cap.read()
            img = cv2.flip(img,1)
            img = detector.get_hand(img,draw_markers=False)
            landmark_list = detector.get_position(img,draw = False,mark_tracker=8)
            if len(landmark_list)!=0:
                finger_tips = np.array([
                    [landmark_list[4][1],landmark_list[4][2]],
                    [landmark_list[8][1],landmark_list[8][2]],
                    [landmark_list[12][1],landmark_list[12][2]],
                    [landmark_list[16][1],landmark_list[16][2]],
                    [landmark_list[20][1],landmark_list[20][2]]
                ])
                landmark_list = np.array(landmark_list)
                x_mean = np.mean(finger_tips[:,0])
                y_mean = np.mean(finger_tips[:,1])
                normalized_finger_tips = (finger_tips - np.array([x_mean,y_mean]))/np.max(np.abs([finger_tips[:,0],finger_tips[:,1]]),axis=1)
                coordinates.append(normalized_finger_tips)
                if len(coordinates) > 10:
                    coordinates.pop(0)
                get_action(coordinates,landmarks=landmark_list)
            # cv2.imshow("Image",cv2.flip(img,1))
            # cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
        return {'FINISHED'}
class CustomizedPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Gesture Panel"
    bl_idname = "OBJECT_PT_random"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Gesture"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator(ButtonOperator.bl_idname,text="Start", icon='VIEW_PAN')


from bpy.utils import register_class,unregister_class


_classes = [
    ButtonOperator,
    CustomizedPanel
]

def register():
    for cls in _classes:
        register_class(cls)

def unregister():
    for cls in _classes:
        unregister_class(cls)

if __name__ == "__main__":
    register()
