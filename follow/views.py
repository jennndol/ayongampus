from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render

from follow.models import Follow


def _friends(request, friends, active, buttons, labels):
    paginator = Paginator(friends, 10)
    clist = zip(friends, buttons, labels)
    page = request.GET.get('page')
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)
    return render(request, 'follow/friends.html', {
        'friends': friends,
        'active': active,
        'clist': clist,
    })


def suggestions(request):
    buttons = []
    labels = []
    suggestions = request.user.profile.get_suggestions()
    for user in suggestions:
        buttons.append(check_following_status(request, user.id))
        labels.append(check_follower_status(request, user.id))
    return _friends(request, suggestions, 'suggestions', buttons, labels)


def followers(request):
    followers = request.user.profile.get_followers()
    labels = []
    buttons = []
    if followers:
        for user in followers:
            buttons.append(check_following_status(request, user.id))
            labels.append(check_follower_status(request, user.id))
    return _friends(request, followers, 'followers', buttons, labels)


def followings(request):
    followings = request.user.profile.get_following()
    buttons = []
    labels = []
    for user in followings:
        buttons.append(check_following_status(request, user.id))
        labels.append(check_follower_status(request, user.id))
    return _friends(request, followings, 'followings', buttons, labels)


def follow(request, id):
    user = request.user
    wanted_user = User.objects.get(id=id)
    if wanted_user != user.id:
        found_user = Follow.objects.filter(following_id=id, user_id=user.id).distinct()
        if not found_user:
            instance = Follow()
            instance.following_id = id
            instance.user_id = user.id
            instance.save()
            messages.add_message(request, messages.SUCCESS, 'User was successfully followed :)')
        else:
            messages.add_message(request, messages.WARNING,
                                 'There''s an unexpected error while trying to follow user :(')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow(request, id):
    wanted_user = User.objects.get(id=id)
    if wanted_user != request.user.id:
        found_user = Follow.objects.filter(following_id=id, user_id=request.user.id).distinct()
        if found_user:
            found_user.delete()
            messages.add_message(request, messages.SUCCESS, 'User was successfully unfollowed :)')
        else:
            messages.add_message(request, messages.WARNING,
                                 'There''s an unexpected error while trying to unfollow user :(')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def check_following_status(request, id):
    is_following = request.user.profile.get_following().filter(id=id)
    if is_following:
        status = 'unfollow'
    else:
        status = 'follow'
    return status


def check_follower_status(request, id):
    is_follower = request.user.profile.get_followers().filter(id=id)
    if is_follower:
        status = 'following'
    else:
        status = 'not following'
    return status
