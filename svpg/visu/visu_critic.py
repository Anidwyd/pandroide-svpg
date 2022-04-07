import random

import matplotlib.pyplot as plt
import numpy as np
import torch as th
from svpg.visu.visu_policies import final_show


def plot_pendulum_critic(
    model, env, plot=True, figname="pendulum_critic.pdf", save_figure=True
) -> None:
    """
    Plot a critic for the Pendulum environment
    :param model: the policy and critic specifying the action to be plotted
    :param env: the evaluation environment
    :param plot: whether the plot should be interactive
    :param figname: the name of the file to save the figure
    :param save_figure: whether the figure should be saved
    :return: nothing
    """
    if env.observation_space.shape[0] <= 2:
        raise (
            ValueError(
                "Observation space dimension {}, should be > 2".format(
                    env.observation_space.shape[0]
                )
            )
        )
    definition = 100
    portrait = np.zeros((definition, definition))
    state_min = env.observation_space.low
    state_max = env.observation_space.high

    for index_t, t in enumerate(np.linspace(-np.pi, np.pi, num=definition)):
        for index_td, td in enumerate(
            np.linspace(state_min[2], state_max[2], num=definition)
        ):
            obs = np.array([[np.cos(t), np.sin(t), td]])
            with th.no_grad():
                obs = th.from_numpy(obs.astype(np.float32))
                value = model(obs).squeeze(-1)

            portrait[definition - (1 + index_td), index_t] = value.item()

    plt.figure(figsize=(10, 10))
    plt.imshow(
        portrait,
        cmap="inferno",
        extent=[-180, 180, state_min[2], state_max[2]],
        aspect="auto",
    )
    plt.colorbar(label="action")
    # Add a point at the center
    plt.scatter([0], [0])
    x_label, y_label = getattr(env.observation_space, "names", ["x", "y"])
    final_show(
        save_figure,
        plot,
        figname,
        x_label,
        y_label,
        "Critic phase portrait",
        "./plots/",
    )


def plot_cartpole_critic(
    model,
    env,
    plot=True,
    figname="cartpole_critic.pdf",
    foldername="./plots/",
    save_figure=True,
) -> None:
    """
    Visualization of the critic in a N-dimensional state space
    The N-dimensional state space is projected into its first two dimensions.
    A FeatureInverter wrapper should be used to select which features to put first so as to plot them
    :param model: the policy and critic to be plotted
    :param env: the environment
    :param plot: whether the plot should be interactive
    :param figname: the name of the file where to plot the function
    :param foldername: the name of the folder where to put the file
    :param save_figure: whether the plot should be saved into a file
    :return: nothing
    """
    if env.observation_space.shape[0] <= 2:
        raise (
            ValueError(
                "Observation space dimension {}, should be > 2".format(
                    env.observation_space.shape[0]
                )
            )
        )
    definition = 100
    portrait = np.zeros((definition, definition))
    state_min = env.observation_space.low
    state_max = env.observation_space.high

    for index_x, x in enumerate(
        np.linspace(state_min[0], state_max[0], num=definition)
    ):
        for index_y, y in enumerate(
            np.linspace(state_min[2], state_max[2], num=definition)
        ):
            obs = np.array([x])
            z1 = random.random() - 0.5
            z2 = random.random() - 0.5
            obs = np.append(obs, z1)
            obs = np.append(obs, y)
            obs = np.append(obs, z2)
            # Add batch dim
            obs = obs.reshape(1, -1)
            with th.no_grad():
                obs = th.from_numpy(obs.astype(np.float32))
                value = model(obs).squeeze(-1)

            portrait[definition - (1 + index_y), index_x] = value.item()

    plt.figure(figsize=(10, 10))
    plt.imshow(
        portrait,
        cmap="inferno",
        extent=[state_min[0], state_max[0], state_min[2], state_max[2]],
        aspect="auto",
    )
    plt.colorbar(label="critic value")
    # Add a point at the center
    plt.scatter([0], [0])
    x_label, y_label = getattr(env.observation_space, "names", ["x", "y"])
    final_show(save_figure, plot, figname, x_label, y_label, "V Function", foldername)