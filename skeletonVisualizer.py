#!/usr/bin/python

import pandas as pd
import os
import Utils
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from math import inf
from matplotlib import collections  as mc

class skeletonVisualizer:


	def __init__(self,src_folder):
		self.skeleton_data = self.load_skeleton_data(src_folder)
	
	def load_skeleton_data(self, src_folder):
		bodyFrame = []
		for file in os.listdir(src_folder):
			if('kinect-skeleton_' in file):
				bodyFrame.append(pd.DataFrame(pd.read_csv(os.path.join(src_folder, file))))
		return bodyFrame
	
	def get_joint_coord_to_link_frame(self,timestamp,idBody,link):
		columns_1 = '{}_x {}_y'.format(link[0],link[0],link[0]).split(' ')
		columns_2 = '{}_x {}_y'.format(link[1],link[1],link[1]).split(' ')
		jcoord_1 = self.skeleton_data[idBody].loc[self.skeleton_data[idBody]['timestamp'] == timestamp, columns_1].values
		jcoord_2 =  self.skeleton_data[idBody].loc[self.skeleton_data[idBody]['timestamp'] == timestamp, columns_2].values
		#return (x1,x2) (y1,y2)
		return [(jcoord_1[0][0],jcoord_2[0][0]),(jcoord_1[0][1],jcoord_2[0][1])]

	def get_joint_coord_to_link_anim(self,i,idBody,link):
		columns_1 = '{}_x {}_y'.format(link[0],link[0],link[0]).split(' ')
		columns_2 = '{}_x {}_y'.format(link[1],link[1],link[1]).split(' ')
		jcoord_1 = self.skeleton_data[idBody].loc[i,columns_1].values
		jcoord_2 =  self.skeleton_data[idBody].loc[i,columns_2].values
		#return (x1,x2) (y1,y2)
		return [(jcoord_1[0],jcoord_2[0]),(jcoord_1[1],jcoord_2[1])]

	#Utility function to find the limits of each dimension Returns:((x min, x_max), (y min, y max), (z min, z max))
	def find_bounds(self):
		column_x = []
		column_y = []
		column_z = []
		body_0 = self.skeleton_data[0]
		body_1 = self.skeleton_data[1]
		for i in Utils.KINECT_JOINTS.keys():
			column_x.append('{}_x'.format(i))
			column_y.append('{}_y'.format(i))

		return (((min(body_0[column_x].min().min(),body_1[column_x].min().min())),  # min(b1_x,b2,x)
				(max(body_0[column_x].max().max(),body_1[column_x].max().max()))),  # max(b1_x,b2,x)
				((min(body_0[column_y].min().min(),body_1[column_y].min().min())),  # min (b1_y,b2_y)
				(max(body_0[column_y].max().max(),body_1[column_y].max().max())))   # max (b1_y,b2_y)
				)
	def initialize_plots(self):
			colors = ('bo-','ro-')
			fig, axes = plt.subplots()
			(x_min, x_max), (y_min, y_max) = self.find_bounds()
			axes.set_xlabel('X')
			axes.set_ylabel('Y')
			axes.set_xlim(left=x_max, right=x_min)
			axes.set_ylim(bottom=y_min, top=y_max)
			plots = []
			for i in range(2):
				color = colors[0] if i == 1 else colors[1]
				plots.append({link: axes.plot([0], [0], color)[0] for link in Utils.skeletonLink})
			return fig, axes,plots
	
	def plot_skeleton_image(self,timestamp):
		fig, ax, plots = self.initialize_plots()
		for link in Utils.skeletonLink:
			jsegment0 = self.get_joint_coord_to_link_frame(timestamp,0,link)
			jsegment1 = self.get_joint_coord_to_link_frame(timestamp,1,link)
			ax.plot(jsegment0[0],jsegment0[1])
			ax.plot(jsegment1[0],jsegment1[1])
		plt.show()

	#TODO
	def plot_animation(self):
		'''Creates an animation from skeleton data'''
		fig,ax,plots = self.initialize_plots()
		
		def init():
			for link in Utils.skeletonLink:
				for i in range(2):
					plots[i][link].set_xdata([0])
					plots[i][link].set_ydata([0])
				return tuple(list(set(plots[0].values()).union(plots[1].values())))

		def animate(i):
			for link in Utils.skeletonLink:
				jsegment0 = self.get_joint_coord_to_link_anim(i,0,link)
				jsegment1 = self.get_joint_coord_to_link_anim(i,1,link)
				#update first body
				xs = (jsegment0[0][0],jsegment0[0][1])
				ys = (jsegment0[1][0],jsegment0[1][1])
				plots[0][link].set_xdata(xs)
				plots[0][link].set_ydata(ys)
				#update second body
				xs = (jsegment1[0][0],jsegment1[0][1])
				ys = (jsegment1[1][0],jsegment1[1][1])
				plots[1][link].set_xdata(xs)
				plots[1][link].set_ydata(ys)
			return tuple(list(set(plots[0].values()).union(plots[1].values())))

		ani = animation.FuncAnimation(fig, animate, init_func=init, 
													frames=self.skeleton_data[0]['timestamp'].count(),
													interval=10,
													blit=True)
		plt.show()

if __name__ == "__main__":
	#skeletonVisualizer('skeleton-data.csv').plot_skeleton_image('0 days 00:00:49.170000000')
	skeletonVisualizer('./data/').plot_animation()