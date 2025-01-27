# -*- coding: utf-8 -*-
"""
Created on Jan 2022

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


import pickle

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CallbackList
from stable_baselines3 import SAC, A2C

# Custom
from env_PaceRace import PaceRaceEnv
from LogTraining import CustomTrainingLogCallback, CustomEvalLogCallback, load_Log 


### CONFIGURATION
config = {'total_timesteps': 200_000,
          'log_keys': ('obs', 'act', 'Fres'),           # custom Train-Logger
          'log_freq_epoch_train': 10,                   # custom Train-Logger
          'log_freq_step_train': 1,                     # custom Train-Logger
          'log_freq_epoch_eval': 1,                     # custom Eval-Logger
          'monitor_log_path': 'TrainLog/DefaultLog',    # integrated Logger
          'save_path_models': "models//sac_pace_race"}

with open('example_eval_tracks.pkl', "rb") as f:  
    eval_center_lines, eval_roadwidths  = pickle.load(f)


### ENV SETUP
env = Monitor(PaceRaceEnv(verbose = 0, ROADLENGTH=10), filename=config['monitor_log_path'])
check_env(env, warn=True)


### MODEL SETUP
model = SAC("MlpPolicy",
            env,
            verbose=1,
            )

# Load pre-trained model
# model = SAC.load("models/sac_pace_race_FL_01_20220122.zip")
# model = SAC.load("models/sac_pace_race_FS_02_210122.zip")
# model = SAC.load("models/sac_pace_race_EM_takethis.zip")
#model.set_env(env)


### CALLBACKS
callback1=CustomTrainingLogCallback(info_keywords = config['log_keys'], 
                                   log_freq_epoch=config['log_freq_epoch_train'], 
                                   log_freq_step=config['log_freq_step_train'])
callback2 = CustomEvalLogCallback(Monitor(PaceRaceEnv()), 
                                  eval_center_lines, 
                                  eval_roadwidths, 
                                  log_freq_epoch=config['log_freq_epoch_eval'])
callback = CallbackList([callback1, callback2])


### TRAINING
print('Start training')
model.learn(config['total_timesteps'], callback=callback)
print('End of training')
env.close()
model.save(config['save_path_models'])


# Load Log
#Log = load_Log('TrainLog/CustomLog')
