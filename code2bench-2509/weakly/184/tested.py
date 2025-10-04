import numpy as np

def get_1d_sincos_pos_embed_from_grid(embed_dim: int, pos: np.ndarray) -> np.ndarray:
    assert (embed_dim % 2) == 0, "Embed dimension must be even"
    omega = np.linspace(0, np.pi / embed_dim, embed_dim // 2)
    pos = pos.reshape(-1)
    out = np.einsum('i,j->ij', pos, omega)
    emb = np.stack([np.sin(out), np.cos(out)], axis=-1)
    return emb.reshape(-1, embed_dim)