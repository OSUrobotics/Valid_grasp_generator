#!/usr/bin/env python
from object_visualizer import *
from std_msgs.msg import Int32MultiArray,String
import numpy as np
import time
import scipy
import pyscreenshot
from scipy import misc
from valid_grasp_generator.srv import *
from Tkinter import *
from symmetricize import reflect_along_x_plane, reflect_along_y_plane, reflect_along_z_plane
import rospkg
import getpass


class VisualizeSimilarGrasps(object):
    def __init__(self):
        self.transform_path = os.path.expanduser("~")+ "/grasping_data"
        self.pkg_path = rospkg.RosPack().get_path('valid_grasp_generator')
        self.camera_transform_path = self.pkg_path+'/essential_files/essential_transform/camera_transform.csv'
        self.camera_transform = np.genfromtxt(self.camera_transform_path,delimiter= ',')
        self.ctrl = object_visualizer()
        self.viewer = self.ctrl.env.GetViewer()
        self.folder_name = self.transform_path+'/output_data_folder/'
        self.folder_list = os.listdir(self.folder_name)
        self.obj_num = 0
        self.filename = None
        self.points = np.array([])

    def update_environment(self):
        for folder in self.folder_list:
            fold = folder.split('_')[0]
            self.obj_num = int(fold[3:])
            cluster_no = folder.split('_')[1]
            user_obj = raw_input('Please Enter object number you want to visualize: ') 
            if self.obj_num  == user_obj:
                files = os.listdir(self.folder_name + "obj" +str(self.obj_num)+"_"+str(cluster_no) +"/")
                self.ctrl.set_obj(self.obj_num)
                sorted_files = []
                for fname in files:
                    if "_HandTransformation" in fname:
                        sorted_files.append(fname)
                
                new_files = sorted(sorted_files)
                
                for j in range(len(new_files)):
                    file_name = new_files[j]
                    sub_idx = file_name.find('_sub')
                    grasp_idx = file_name.find('_grasp')
                    sub_num = int(file_name[sub_idx+4:grasp_idx])
                    idx = file_name.find('_Hand')
                    filename =file_name[:idx]
                    f = self.folder_name +"obj"+str(self.obj_num)+'_'+str(cluster_no)+"/" +  filename
                    rospy.loginfo("Showing " + f)
                    T_hand = np.genfromtxt(f+"_HandTransformation.txt",delimiter = ',')
                    T_obj = np.genfromtxt(f+"_ObjTransformation.txt",delimiter = ',')
                    _ = self.ctrl.reorient_hand(T_hand, T_obj)
                    joint_angles = np.genfromtxt(f+"_JointAngles.txt",delimiter = ',') #for barrett arm
                    self.ctrl.set_joint_angles(joint_angles)
                    contact_links = np.genfromtxt(f+"_ContactLinkNames.txt",delimiter = ',',dtype = '|S')
                    self.points = np.genfromtxt(f+"_contactpoints.txt",delimiter = ',')
                    self.ctrl.PlotPoints(self.points)
                    self.filename = 'obj'+str(self.obj_num) +'_'+cluster_no+file_name[sub_idx:]
                    print
                    raw_input('Press Enter to continue')

    def execute_command(self,data):
        rospy.loginfo('Command Received: %s',data.data)
        if data.data == 'reflect_x':
            reflect_along_x_plane(self.ctrl.env,self.ctrl.hand_1)
        elif data.data == 'reflect_y':
            reflect_along_y_plane(self.ctrl.env,self.ctrl.hand_1)
        elif data.data == 'reflect_z':
            reflect_along_z_plane(self.ctrl.env,self.ctrl.hand_1)
        elif data.data == 'plot_contact_points':
            self.ctrl.PlotPoints(self.points)
        elif data.data == 'reorient_camera':
            self.camera_transform = np.genfromtxt(self.camera_transform_path,delimiter= ',')
            self.viewer.SetCamera(self.camera_transform)
        elif data.data == 'retract_fingers':
            self,points,_ = self.ctrl.avoid_hand_collision()
        elif data.data == 'take_picture':
            take_image = rospy.ServiceProxy('take_snap_shot',SnapShot)
            take_image('/home/'+getpass.getuser()+'/similar_grasp_images/'+self.filename+'.jpg')
        elif data.data == 'save_new_camera_transform':
            np.savetxt(self.camera_transform_path,self.viewer.GetCameraTransform(),delimiter=',')





if __name__ == "__main__":
    rospy.init_node('visualize_similar_grasp',anonymous = True)
    visualize_grasps = VisualizeSimilarGrasps()
    subscriber_commander = rospy.Subscriber('Modify_and_snapshot', String, visualize_grasps.execute_command)
    visualize_grasps.update_environment()

