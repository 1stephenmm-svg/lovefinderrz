from storage import save_like


def get_client_likes(client_id, likes):
    likes_sent = []
    likes_received = []

    for sender_id, receiver_id in likes:
        if sender_id == client_id:
            likes_sent.append(receiver_id)
        if receiver_id == client_id:
            likes_received.append(sender_id)

    return likes_sent, likes_received


def register_like(client_id, liked_client_id, likes):
    """Register a like if it has not been registered before."""
    like = (client_id, liked_client_id)

    if like in likes:
        return False

    save_like(client_id, liked_client_id)
    likes.append(like)

    return True
