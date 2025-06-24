from core.models import Profile

num_profiles = Profile.objects.count()

print(f"Number of profiles: {num_profiles}")
