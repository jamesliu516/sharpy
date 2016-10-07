# Alfonso del Carre
# alfonso.del-carre14@imperial.ac.uk
# Imperial College London
# LoCA lab
# 28 Sept 2016

# preSHARPy is the FEM and aero data preprocessor for the SHARPy code
# It reads the information from *.fem.h5 and *.aero.h5 files.

import h5py as h5
import numpy as np
import configparser

import h5utils
import aerogrid.aerogrid as aerogrid
import beam.beam as beam

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



class ProblemData(object):

    # Reads the FEM and aero files and stores them in
    # the class instance.
    def __init__(self, in_case_name, in_case_route = './'):
        '''
        AERO SUPPORT IN PROGRESS
        '''
        print('Reading input info for the case: %s in %s...'%(in_case_name,
                                                              in_case_route))
        self.case_route = in_case_route
        self.case_name = in_case_name
        fem_file_name = in_case_route + '/' +  in_case_name + '.fem.h5'
        aero_file_name = in_case_route + '/' +  in_case_name + '.aero.h5'

        # Check if files exist
        h5utils.check_file_exists(fem_file_name)
        h5utils.check_file_exists(aero_file_name)
        print('\tThe FEM and aero files exist, they will be loaded.')

        # Assign handles
        # !!!
        # These handles are stored in the class.
        # That means that they will stay open until
        # we manually close them or the instance of
        # ProblemData is destroyed
        self.fem_handle = h5.File(fem_file_name, 'r')
        self.aero_handle = h5.File(aero_file_name, 'r')

        # Store h5 info in dictionaries
        self.fem_data_dict = (
            h5utils.load_h5_in_dict(self.fem_handle))
        h5utils.check_fem_dict(self.fem_data_dict)

        self.aero_data_dict = (
            h5utils.load_h5_in_dict(self.aero_handle))
        # h5utils.check_aero_dict(self.aero_data_dict)   #TODO

        # FLIGHT CONDITIONS and SOLVER settings files input
        flightcon_file_name = (in_case_route + '/' +
                               in_case_name + '.flightcon.txt')
        solver_file_name = in_case_route + '/' +  in_case_name + '.solver.txt'
        # Check if files exist
        h5utils.check_file_exists(flightcon_file_name)
        h5utils.check_file_exists(solver_file_name)
        print('\tThe FLIGHTCON and SOLVER files exist, they will be loaded.')
        self.flightcon_config = self.load_config_file(flightcon_file_name)
        self.solver_config = self.load_config_file(solver_file_name)

        # import pdb;pdb.set_trace()
        print('\tDONE')
        print('--------------------------------------------------------------')
        print('Processing fem input and generating beam model...')
        self.beam = beam.Beam(self.fem_data_dict)
        print('Processing aero input and generating grid...')
        ProblemData.grid = aerogrid.AeroGrid(self.aero_data_dict,
                                             self.solver_config,
                                             self.flightcon_config,
                                             self.beam)


    def load_config_file(self, file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        return config



    def plot_configuration(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title('Case: %s -- structure plot'%self.case_name)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_zlabel('z (m)')

        self.beam.plot(fig, ax)
        # self.plot_aero(fig, ax)

        plt.show()

    # def plot_fem(self, fig=None, ax=None):
        # if fig == None:
            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            # plt.title('Case: %s -- structure plot'%self.case_name)
            # ax.set_xlabel('x (m)')
            # ax.set_ylabel('y (m)')
            # ax.set_zlabel('z (m)')
        # plt.hold('on')
        # # nodes plot
        # nodes = ax.scatter(self.fem_data_dict['coordinates'][:,0],
                           # self.fem_data_dict['coordinates'][:,1],
                           # self.fem_data_dict['coordinates'][:,2])

        # colors = ['k', 'b', 'r', 'y']
        # # elements plot
        # for ielem in range(self.fem_data_dict['num_elem']):
            # ax.plot(self.fem_data_dict['coordinates']
                        # [self.fem_data_dict['connectivities'][ielem,:],0],
                    # self.fem_data_dict['coordinates']
                        # [self.fem_data_dict['connectivities'][ielem,:],1],
                    # self.fem_data_dict['coordinates']
                        # [self.fem_data_dict['connectivities'][ielem,:],2],
                    # linewidth=3*1/(self.fem_data_dict['elem_stiffness'][ielem]+1),
                    # color=colors[self.fem_data_dict['elem_mass'][ielem]])

        # plt.hold('off')
        # return fig, ax


    def plot_aero(self, fig=None, ax=None):
        if fig == None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            plt.title('Case: %s -- structure plot'%self.case_name)
            ax.set_xlabel('x (m)')
            ax.set_ylabel('y (m)')
            ax.set_zlabel('z (m)')
        plt.hold('on')




        plt.hold('off')
        return fig, ax

if __name__ == '__main__':
    problem = ProblemData('test', './test_data/')
    problem.plot_configuration()
    # print(problem.aero_data_dict)
