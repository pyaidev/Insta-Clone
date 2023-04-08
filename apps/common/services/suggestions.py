from django.db.models import Q
from apps.users.models import User
from apps.profiles.models import Profile


def get_main_suggestions(user_id):
    user = User.objects.get(id=user_id)

    main_suggestions = Profile.objects.filter(
        Q()
    )

    extra_suggestions = Profile.objects.filter(
        Q(followers__followed_by__followers_followed_by__user=user) |
        Q(followings__followed_to__followers_followed_by__user=user)
    )
