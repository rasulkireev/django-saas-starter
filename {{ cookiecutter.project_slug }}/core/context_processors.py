from core.choices import ProfileStates


def current_state(request):
    if request.user.is_authenticated:
        return {"current_state": request.user.profile.current_state}
    return {"current_state": ProfileStates.STRANGER}
