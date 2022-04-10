import numpy as np

from svpg.algos.algo import Algo


class A2C(Algo):
    def __init__(self, cfg):
        super().__init__(cfg)

    def compute_critic_loss(self, reward, done, critic):
        # Compute TD error
        target = reward[1:] + self.discount_factor * critic[1:].detach() * (
            1 - done[1:].float()
        )
        td = target - critic[:-1]
        # Compute critic loss
        td_error = td ** 2
        critic_loss = td_error.mean()

        return critic_loss, td

    def compute_policy_loss(self, action_logprobs, td):
        policy_loss = action_logprobs[:-1] * td.detach()

        return policy_loss.mean()

    def compute_loss(self, workspaces, logger, epoch, alpha=10, verbose=True):
        total_critic_loss, total_entropy_loss, total_policy_loss = 0, 0, 0
        rewards = np.zeros(self.n_particles)

        for pid in range(self.n_particles):
            # Extracting the relevant tensors from the workspace
            critic, done, action_logprobs, reward, entropy = workspaces[pid][
                "critic", "env/done", "action_logprobs", "env/reward", "entropy"
            ]

            # Compute loss
            critic_loss, td = self.compute_critic_loss(reward, done, critic)
            total_critic_loss = total_critic_loss + critic_loss

            total_entropy_loss = total_entropy_loss + entropy.mean()

            if alpha is not None:
                total_policy_loss = total_policy_loss - self.compute_policy_loss(
                    action_logprobs, td
                ) * (1 / alpha) * (1 / self.n_particles)
            else:
                total_policy_loss = total_policy_loss - self.compute_policy_loss(
                    action_logprobs, td
                )

            # Log reward
            creward = workspaces[pid]["env/cumulated_reward"]
            creward = creward[done]

            rewards[pid] = creward.mean()

            if creward.size()[0] > 0:
                logger.add_log(f"reward_{pid}", rewards[pid], epoch)

        if verbose:
            logger.log_losses(
                epoch, total_critic_loss, total_entropy_loss, total_policy_loss
            )

        return total_critic_loss, total_entropy_loss, total_policy_loss, rewards
