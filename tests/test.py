import hydra
from hydra.utils import instantiate

from svpg.algos.svpg import SVPG

from omegaconf import OmegaConf

import matplotlib.pyplot as plt
import numpy as np
import datetime
from pathlib import Path

from svpg.common.visu import plot_algo_policies, plot_histograms

try:
    OmegaConf.register_new_resolver("get_method", hydra.utils.get_method)
except:
    print("Already register")

import os


@hydra.main(config_path=".", config_name="test_a2c.yaml")
def main(cfg):
    import torch.multiprocessing as mp

    try:
        mp.set_start_method("spawn")
    except:
        pass

    d = datetime.datetime.today()
    directory = d.strftime(str(Path(__file__).parents[1]) + "/archives/%m-%d_%H-%M/")

    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("directory existed")

    env = instantiate(cfg.algorithm.env)
    env_name = cfg.env_name

    # --------- A2C INDEPENDENT --------- #
    algo_a2c = instantiate(cfg.algorithm)
    algo_a2c.run()

if __name__ == "__main__":
    main()
