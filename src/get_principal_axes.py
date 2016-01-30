#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from draw_arrow import Arrow3D

def GetPrincipalAxes(points):
    cov_mat = np.cov([points[:,0],points[:,1],points[:,2]])
    eig_val_cv, eig_vec_cv = np.linalg.eig(cov_mat)
    mean_vec = np.mean(points,axis=0)
    scatter_matrix = np.zeros((3,3))
    for i in range(points.shape[0]):
        value = np.dot(np.array([(points[i,:] - mean_vec)]).T,np.array([(points[i,:] - mean_vec)]))
        scatter_matrix += value
    eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix)
    assert eig_vec_sc.all() == eig_vec_cv.all(), 'Eigenvectors are not identical'
    return eig_val_sc,eig_vec_sc

if __name__ == "__main__":
    #np.random.seed(1) # random seed for consistency
    #
    #mu_vec1 = np.array([0,0,0])
    #cov_mat1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
    #class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 20).T
    #assert class1_sample.shape == (3,20), "The matrix has not the dimensions 3x20"
    #
    #mu_vec2 = np.array([1,1,1])
    #cov_mat2 = np.array([[1,0,0],[0,1,0],[0,0,1]])
    #class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 20).T
    #assert class1_sample.shape == (3,20), "The matrix has not the dimensions 3x20"
    #points = np.concatenate((class1_sample, class2_sample),axis=1).T

    points = np.array([[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]])
    eigen_val,vector = GetPrincipalAxes(points)
    print "You can check the points and respective principal axis on the map" 
    fig = plt.figure()
    print "vector: ", vector
    mean_vec = np.mean(points,axis=0)
    ax = fig.add_subplot(111,projection = "3d")
    ax.scatter(points[:,0],points[:,1],points[:,2], label = '3d object')
    for vec in vector:
        a = Arrow3D([mean_vec[0], vec[0]+mean_vec[0]],[mean_vec[1], vec[1]+mean_vec[1]],[mean_vec[2],vec[2]+mean_vec[2]], mutation_scale = 20, lw=3, arrowstyle = "-|>", color="r")
        ax.add_artist(a)
    ax.legend()
    plt.show()
