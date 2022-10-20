from .models import CollabRequest, Profile


def find_collabs(user):
    """
    Retrieves profiles of users with a pending collab request
    for the specified user
    """
    # Find collab reqeusts sent to and from user
    collab_requests_from_user = CollabRequest.objects.filter(
            from_user=user
        )
    collab_requests_to_user = CollabRequest.objects.filter(
            to_user=user
        )
    # Find the other party assoicated with these collab requests
    collab_request_users = []
    for collab_request in collab_requests_from_user:
        collab_request_users.append(collab_request.to_user)
    for collab_request in collab_requests_to_user:
        collab_request_users.append(collab_request.from_user)

    return collab_request_users
