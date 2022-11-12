import torch
from dalle2_pytorch import DiffusionPriorNetwork, DiffusionPrior, CLIP
from accessify import private


@private
def get_new_diffusion_prior_network():
    return DiffusionPriorNetwork(
        dim=512,
        depth=6,
        dim_head=64,
        heads=8
    ).cuda()


@private
def get_diffusion_prior_network(clip, prior_network):
    return DiffusionPrior(
        net=prior_network,
        clip=clip,
        timesteps=100,
        cond_drop_prob=0.2
    ).cuda()


@private
def get_data():
    text = torch.randint(0, 49408, (4, 256)).cuda()
    images = torch.randn(4, 3, 256, 256).cuda()
    return text, images


def get_prior_network(clip):
    # setup prior network, which contains an autoregressive transformer
    prior_network = get_new_diffusion_prior_network()

    # diffusion prior network, which contains the CLIP and network (with transformer) above

    diffusion_prior = get_diffusion_prior_network(clip, prior_network)

    # mock data
    text, images = get_data()

    clip_image_embeds = diffusion_prior.clip.embed_image(images).image_embed
    clip_text_embeds = diffusion_prior.clip.embed_text(text).text_embed

    # feed text and images into diffusion prior network
    loss = diffusion_prior(
        text_embed=clip_text_embeds,
        image_embed=clip_image_embeds
    )
    # or
    # loss = diffusion_prior(text,images)

    loss.backward()
    return diffusion_prior
