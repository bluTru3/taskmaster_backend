from taskmaster_mitten.models import Task


def get_user_tasks(user, query_params):
    queryset = Task.objects.filter(owner=user)
    status_value = query_params.get("status")
    search_value = query_params.get("q")

    if status_value:
        queryset = queryset.filter(status=status_value)

    if search_value:
        queryset = queryset.filter(title__icontains=search_value) | queryset.filter(
            description__icontains=search_value
        )

    return queryset.distinct()
