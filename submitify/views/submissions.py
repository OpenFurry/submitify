import os
import pypandoc
import re
import shutil
import subprocess
import tempfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.template.loader import render_to_string

from submitify.forms import (
    ReviewForm,
    SubmissionForm,
)
from submitify.models import (
    Call,
    Notification,
    Review,
    Submission,
)


def manuscriptify(instance):
    tempdir = tempfile.mkdtemp()
    contents = pypandoc.convert_file(instance.original_file.name, 'latex')
    rendered = render_to_string('submitify/manuscript.tex', context={
        'call': instance.call.title,
        'title': instance.title,
        'contents': contents,
    })
    with open(os.path.join(tempdir, 'manuscript.tex'), 'w') as f:
        f.write(rendered)
        subprocess.call([
            'pdflatex',
            '-output-directory',
            tempdir,
            os.path.join(tempdir, 'manuscript.tex')
        ])
        file_dir = os.path.dirname(
            os.path.abspath(instance.original_file.path))
        with open(os.path.join(tempdir, 'manuscript.pdf'), 'rb') as outfile:
            instance.submission_file.save(
                os.path.join(file_dir, '{}.pdf'.format(instance.id)),
                outfile,
                save=False)
    shutil.rmtree(tempdir, True)

@login_required
def create_submission(request, call_id=None, call_slug=None):
    call = get_object_or_404(Call, pk=call_id)
    notifications = Notification.objects.filter(
        call=call, targets__in=[request.user])
    can_submit = True
    if (call.restricted_to.count() > 0 and
            request.user not in call.restricted_to.all()):
        can_submit = False
    elif (not call.readers_can_submit and request.user in call.readers.all()):
        can_submit = False
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.call = call
            submission.owner = request.user
            submission.save()
            form.save_m2m()
            manuscriptify(submission)
            submission.save(process_file=True)
            messages.success(request, 'Work submitted!')
            return redirect(call.get_absolute_url())
    return render(request, 'submitify/calls/view.html', {
        'title': call.title,
        'subtitle': 'Call for submissions',
        'call': call,
        'can_submit': can_submit,
        'form': form,
        'with_submissions': request.user in call.readers.all(),
        'notifications': notifications,
    })


@login_required
def view_submission(request, call_id=None, call_slug=None,
                    submission_id=None):
    call = get_object_or_404(Call, pk=call_id)
    submission = get_object_or_404(Submission, pk=submission_id, call=call)
    if not (request.user in call.readers.all() or request.user == call.owner):
        messages.error(request, "Only users listed as that call's readers "
                       "may view submissions for that call.")
        return render(request, 'submitify/permission_denied.html', {}, status=403)
    try:
        review = Review.objects.get(submission=submission, owner=request.user)
    except Review.DoesNotExist:
        review = None
    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.submission = submission
            review.save()
            form.save_m2m()
            return redirect(submission.get_absolute_url())
    return render(request, 'submitify/submissions/view.html', {
        'title': submission.title,
        'call': call,
        'form': form,
        'review': review,
        'submission': submission,
    })


@login_required
def view_submission_text(request, call_id=None, call_slug=None,
                         submission_id=None):
    call = get_object_or_404(Call, pk=call_id)
    submission = get_object_or_404(Submission, pk=submission_id, call=call)
    if not (request.user in call.readers.all() or request.user == call.owner):
        messages.error(request, "Only users listed as that call's readers "
                       "may view submissions for that call.")
        return render(request, 'submitify/permission_denied.html', {}, status=403)
    return render(request, 'submitify/submissions/view_text.html', {
        'submission': submission,
    })


@login_required
def view_submission_file(request, call_id=None, call_slug=None,
                         submission_id=None):
    call = get_object_or_404(Call, pk=call_id)
    submission = get_object_or_404(Submission, pk=submission_id, call=call)
    if not (request.user in call.readers.all() or request.user == call.owner):
        messages.error(request, "Only users listed as that call's readers "
                       "may view submissions for that call.")
        return render(request, 'permission_denied.html', {}, status=403)
    import pdb; pdb.set_trace()
    with open(submission.submission_file, 'rb') as f:
        contents = f.read()
    return HttpResponse(contents, content_type='application/pdf')


@login_required
def accept_submission(request, call_id=None, call_slug=None,
                      submission_id=None):
     call = get_object_or_404(Call, pk=call_id)
     if call.status != Call.CLOSED_REVIEWING:
         messages.error(request, 'You may only accept submissions when '
                        'reviewing is completed')
         return render(request, 'submitify/permission_denied.html', {}, status=403)
     submission = get_object_or_404(Submission, pk=submission_id, call=call)
     submission.status = Submission.ACCEPTED
     return redirect(submission.get_absolute_url())


@login_required
def reject_submission(request, call_id=None, call_slug=None,
                      submission_id=None):
     call = get_object_or_404(Call, pk=call_id)
     if call.status != Call.CLOSED_REVIEWING:
         messages.error(request, 'You may only accept submissions when '
                        'reviewing is completed')
         return render(request, 'submitify/permission_denied.html', {}, status=403)
     submission = get_object_or_404(Submission, pk=submission_id, call=call)
     submission.status = Submission.ACCEPTED
     return redirect(submission.get_absolute_url())
