from django.shortcuts import render, reverse
from django.views.generic import UpdateView
from .models import Profile, Dweet
from .forms import DweetFrom, UserForm
from django.shortcuts import redirect
# Create your views here.


def dashboard(request):
    form = DweetFrom(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("created_at")

    return render(
        request, 'dwitter/dashboard.html',
        {"form": form, "dweets":followed_dweets},
    )


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'dwitter/profile_list.html', {'profiles': profiles})


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)

    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, 'dwitter/profile.html', {'profile': profile})


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = UserForm
    template_name = 'edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('dwitter:profile', kwargs={'pk': self.object.pk})


