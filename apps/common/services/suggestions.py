from django.db.models import Q

from apps.users.models import User
from apps.profiles.models import Profile


def get_main_suggestions(user_id):
    user_profile = User.objects.get(id=user_id).profile

    suggestion_profiles = Profile.objects.filter(
        Q(followers__followed_by__followings__followed_to=user_profile) |
        Q(followings__followed_to__followers__followed_by=user_profile)
    ).exclude(
        Q(user_id=user_id) | Q(followers__followed_by=user_profile)
    )

    count = suggestion_profiles.count()
    if count < 30:
        new_profiles = Profile.objects.exclude(
            Q(user_id=user_id) | Q(followers__followed_by=user_profile)
        ).order_by('-created_at')[:(30-count)]
        suggestion_profiles = suggestion_profiles | new_profiles

    return suggestion_profiles.distinct()
