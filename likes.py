from storage import save_like


def register_like(client_id, liked_client_id, likes):
    """Register a like if it has not been registered before."""
    like = (client_id, liked_client_id)

    if like in likes:
        return False

    save_like(client_id, liked_client_id)
    likes.append(like)

    return True
