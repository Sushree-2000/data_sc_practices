# Reinforcement Learning pseudocode
"""
obs = env.reset()
h= mdnrnn.initial_state
done=False
cumulative_reward=0
while not done:
    z = cnnvae(obs)
    a = controller([z,h])
    obs, reward, done = env.step(a)
    cumulative_reward += reward
    h = mdnrnn([a,z,h])
"""
# import gym first with command::  "python -m pip install gymnasium"
import gym
import numpy as np
import tensorflow as tf

env = gym.make("CartPole-v1")
obs = env.reset()

h = sess.run(mdnrnn.initial_state)
done = False

while not done:
    z = sess.run(cnnvae.z, feed_dict={cnnvae.x: obs[None]})
    a = controller(z, h)   # controller should be pure numpy
    obs, reward, done, _ = env.step(a)
    h = sess.run(
        mdnrnn.final_state,
        feed_dict={
            mdnrnn.input_z: z,
            mdnrnn.input_a: a,
            mdnrnn.initial_state: h
        }
    )
