def find_compatible_clients(current_client, clients):
    compatible_clients = []

    if not current_client:
        return clients

    for client in clients:
        if client == current_client:
            continue

        if not client.is_active or client.is_blocked:
            continue

        if (
            current_client.same_orientation
            and client.orientation != current_client.orientation
        ):
            continue

        if (
            current_client.same_orientation
            and client.gender == current_client.gender
        ):
            continue

        if (
            current_client.same_location
            and client.city != current_client.city
        ):
            continue

        compatible_clients.append(client)

    return compatible_clients