import torch
from dalle2_pytorch import Unet, Decoder, CLIP
from accessify import private


@private
def get_new_unet1():
    return Unet(
        dim=128,
        image_embed_dim=512,
        text_embed_dim=512,
        cond_dim=128,
        channels=3,
        dim_mults=(1, 2, 4, 8),
        cond_on_text_encodings=True  # set to True for any unets that need to be conditioned on text encodings
    ).cuda()


@private
def get_new_unet2():
    return Unet(
        dim=16,
        image_embed_dim=512,
        cond_dim=128,
        channels=3,
        dim_mults=(1, 2, 4, 8, 16)
    ).cuda()


@private
def get_new_decoder(unets, clip):
    return Decoder(
        unet=unets,
        image_sizes=(128, 256),
        clip=clip,
        timesteps=100,
        image_cond_drop_prob=0.1,
        text_cond_drop_prob=0.5
    ).cuda()


@private
def get_data():
    text = torch.randint(0, 49408, (4, 256)).cuda()
    images = torch.randn(4, 3, 256, 256).cuda()
    return text, images


def get_new_unets():
    return get_new_unet1(), get_new_unet2()


def get_trained_decoder(clip):
    # unet for the decoder
    unets = get_new_unets()

    # decoder, which contains the unet and clip
    decoder = get_new_decoder(unets, clip)

    # mock images (get a lot of this)
    text, images = get_data()

    # feed images into decoder
    loss = decoder(images, text, unet_number=1)
    loss.backward()
    loss = decoder(images, text, unet_number=2)
    loss.backward()
    #     or by 4 chapter https://github.com/lucidrains/DALLE2-pytorch
    #     loss = decoder(images, unet_number=1)
    #     loss.backward()
    #     loss = decoder(images, unet_number=2)
    #     loss.backward()
    #
    return decoder

    # do the above for many many many many steps
    # then it will learn to generate images based on the CLIP image embeddings
