import setup_path
import airsim
import numpy as np
import math
import time
from argparse import ArgumentParser

import gym
from gym import spaces
from airgym.envs.airsim_env import AirSimEnv


class AirSimDroneEnv(AirSimEnv):
    stepNumber = 0

    def __init__(self, ip_address, step_length, image_shape):
        super().__init__(image_shape)
        self.step_length = step_length
        self.image_shape = image_shape

        self.state = {
            "position": np.zeros(3),
            "collision": False,
            "prev_position": np.zeros(3),
        }

        self.drone = airsim.MultirotorClient(ip=ip_address)
        self.action_space = spaces.Discrete(7)
        self._setup_flight()

        self.image_request = airsim.ImageRequest(
            3, airsim.ImageType.DepthPerspective, True, False
        )

    def __del__(self):
        self.drone.reset()

    def _setup_flight(self):
        self.drone.reset()
        self.drone.enableApiControl(True)
        self.drone.armDisarm(True)

        # Set home position and velocity
        self.drone.moveToPositionAsync(-10, 10, -10, 10).join()
        # self.drone.moveByVelocityAsync(1, -0.67, -0.8, 5).join()

    def transform_obs(self, responses):
        img1d = np.array(responses[0].image_data_float, dtype=np.float)
        img1d = 255 / np.maximum(np.ones(img1d.size), img1d)
        img2d = np.reshape(img1d, (responses[0].height, responses[0].width))

        from PIL import Image

        image = Image.fromarray(img2d)
        im_final = np.array(image.resize((84, 84)).convert("L"))

        return im_final.reshape([84, 84, 1])

    def _get_obs(self):
        responses = self.drone.simGetImages([self.image_request])
        image = self.transform_obs(responses)
        self.drone_state = self.drone.getMultirotorState()

        self.state["prev_position"] = self.state["position"]
        self.state["position"] = self.drone_state.kinematics_estimated.position
        self.state["velocity"] = self.drone_state.kinematics_estimated.linear_velocity

        collision = self.drone.simGetCollisionInfo().has_collided
        self.state["collision"] = collision

        return image

    def _do_action(self, action):
        quad_offset = self.interpret_action(action)
        quad_vel = self.drone.getMultirotorState().kinematics_estimated.linear_velocity
        self.drone.moveByVelocityAsync(
            quad_vel.x_val + quad_offset[0],
            quad_vel.y_val + quad_offset[1],
            quad_vel.z_val + quad_offset[2],
            5,
        ).join()

    def _compute_reward(self):
        quad_pt = np.array(
            list(
                (
                    self.state["position"].x_val,
                    self.state["position"].y_val,
                    self.state["position"].z_val,
                )
            )
        )
        goal = np.array(list((-30, 30, -30)))
        
        if np.array_equal(goal, quad_pt):
            done = 1
            reward = 30
            return reward, done
        else:
            done = 0
        
        distance = abs(math.sqrt(math.pow(quad_pt[0] - goal[0], 2) + math.pow(quad_pt[1] - goal[1], 2) + math.pow(quad_pt[2] - goal[2], 2)* 1.0))
        
        if distance > 30:
            reward = -20
        else:
            reward = (30 - distance) * 0.1
        
        return reward, done
    
    """
        xCoordinate = -(10 + (AirSimDroneEnv.stepNumber * self.step_length))
        yCoordinate = 10 + (AirSimDroneEnv.stepNumber * self.step_length)
        zCoordinate = -(5 + (AirSimDroneEnv.stepNumber * self.step_length))
        goal = np.array(list((xCoordinate, yCoordinate, zCoordinate)))
        
        print("XCoordinate: ", xCoordinate)
        print("YCoordinate: ", yCoordinate)
        print("ZCoordinate: ", zCoordinate)

        quad_pt = np.array(
            list(
                (
                    self.state["position"].x_val,
                    self.state["position"].y_val,
                    self.state["position"].z_val,
                )
            )
        )
        
        print("quad_pt X: ", quad_pt[0])
        print("quad_pt Y: ", quad_pt[1])
        print("quad_pt Z: ", quad_pt[2])
        
        distance = abs(math.sqrt(math.pow(quad_pt[0] - goal[0], 2) + math.pow(quad_pt[1] - goal[1], 2) + math.pow(quad_pt[2] - goal[2], 2)* 1.0))
        
        print("Distance: ", distance)

        if distance == 0:
            reward = 100
        elif distance <= 10:
            reward = 20
        elif distance <= 20:
            reward = -distance
        else:
            reward = -100
        
        AirSimDroneEnv.stepNumber += 1

        done = 0
        if (np.array_equal(goal, quad_pt)):
            done = 1
            AirSimDroneEnv.stepNumber = 0
        
        elif (AirSimDroneEnv.stepNumber >= 20):
            AirSimDroneEnv.stepNumber = 0

        return reward, done
"""
    def step(self, action):
        self._do_action(action)
        obs = self._get_obs()
        reward, done = self._compute_reward()

        return obs, reward, done, self.state

    def reset(self):
        self._setup_flight()
        return self._get_obs()

    def interpret_action(self, action):
        if action == 0:
            quad_offset = (self.step_length, 0, 0)
        elif action == 1:
            quad_offset = (0, self.step_length, 0)
        elif action == 2:
            quad_offset = (0, 0, self.step_length)
        elif action == 3:
            quad_offset = (-self.step_length, 0, 0)
        elif action == 4:
            quad_offset = (0, -self.step_length, 0)
        elif action == 5:
            quad_offset = (0, 0, -self.step_length)
        else:
            quad_offset = (0, 0, 0)

        return quad_offset
