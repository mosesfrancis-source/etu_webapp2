from django.utils import timezone
from .models import Message, Notification, Assignment, Announcement, ExamSchedule


def portal_context(request):
    if not request.user.is_authenticated:
        return {'unread_messages': 0, 'unread_notifications': 0,
                'activity_dues': [], 'activity_recent': []}

    unread = Message.objects.filter(recipient=request.user, is_read=False).count()
    alerts = Notification.objects.filter(user=request.user, is_read=False).count()

    now = timezone.now()
    soon = now + timezone.timedelta(days=14)

    dues = []
    recent = []

    if request.user.role == 'student':
        # Courses the student is registered for
        from courses.models import CourseRegistration
        reg_course_ids = CourseRegistration.objects.filter(
            student=request.user, status='approved'
        ).values_list('course_id', flat=True)

        # Upcoming assignment due dates
        upcoming_assignments = (
            Assignment.objects
            .filter(course_id__in=reg_course_ids, due_date__gte=now, due_date__lte=soon, is_published=True)
            .select_related('course')
            .order_by('due_date')[:5]
        )
        for a in upcoming_assignments:
            delta = a.due_date - now
            dues.append({
                'type': 'assignment',
                'icon': 'bi-journal-check',
                'color': 'warning' if delta.days <= 2 else 'primary',
                'label': a.title,
                'course': a.course.code,
                'due': a.due_date,
                'days_left': delta.days,
            })

        # Upcoming exams/tests
        upcoming_exams = (
            ExamSchedule.objects
            .filter(course_id__in=reg_course_ids, scheduled_for__gte=now, scheduled_for__lte=soon, is_published=True)
            .select_related('course')
            .order_by('scheduled_for')[:3]
        )
        for e in upcoming_exams:
            delta = e.scheduled_for - now
            dues.append({
                'type': 'exam',
                'icon': 'bi-clipboard-data',
                'color': 'danger' if delta.days <= 2 else 'info',
                'label': e.title,
                'course': e.course.code,
                'due': e.scheduled_for,
                'days_left': delta.days,
            })

        dues.sort(key=lambda x: x['due'])

        # Recent activities — last 6 items
        recent_assignments = (
            Assignment.objects
            .filter(course_id__in=reg_course_ids, is_published=True)
            .select_related('course')
            .order_by('-published_at')[:3]
        )
        for a in recent_assignments:
            recent.append({
                'icon': 'bi-journal-check',
                'color': 'warning',
                'text': f"New assignment: {a.title}",
                'sub': a.course.code,
                'time': a.published_at,
            })

        recent_announcements = (
            Announcement.objects
            .filter(is_active=True)
            .order_by('-created_at')[:3]
        )
        for ann in recent_announcements:
            if ann.is_visible_to(request.user):
                recent.append({
                    'icon': 'bi-megaphone-fill',
                    'color': 'info',
                    'text': ann.title,
                    'sub': 'Announcement',
                    'time': ann.created_at,
                })

        recent.sort(key=lambda x: x['time'], reverse=True)
        recent = recent[:5]

    elif request.user.role in ('lecturer', 'hod'):
        from courses.models import Course
        course_ids = Course.objects.filter(lecturer=request.user, is_active=True).values_list('id', flat=True)

        upcoming_exams = (
            ExamSchedule.objects
            .filter(course_id__in=course_ids, scheduled_for__gte=now, scheduled_for__lte=soon, is_published=True)
            .select_related('course')
            .order_by('scheduled_for')[:5]
        )
        for e in upcoming_exams:
            delta = e.scheduled_for - now
            dues.append({
                'type': 'exam',
                'icon': 'bi-clipboard-data',
                'color': 'danger' if delta.days <= 2 else 'primary',
                'label': e.title,
                'course': e.course.code,
                'due': e.scheduled_for,
                'days_left': delta.days,
            })

        upcoming_assignments = (
            Assignment.objects
            .filter(course_id__in=course_ids, due_date__gte=now, due_date__lte=soon, is_published=True)
            .select_related('course')
            .order_by('due_date')[:5]
        )
        for a in upcoming_assignments:
            delta = a.due_date - now
            dues.append({
                'type': 'assignment',
                'icon': 'bi-journal-check',
                'color': 'warning' if delta.days <= 2 else 'success',
                'label': a.title,
                'course': a.course.code,
                'due': a.due_date,
                'days_left': delta.days,
            })

        dues.sort(key=lambda x: x['due'])

        recent_announcements = (
            Announcement.objects
            .filter(is_active=True)
            .order_by('-created_at')[:5]
        )
        for ann in recent_announcements:
            recent.append({
                'icon': 'bi-megaphone-fill',
                'color': 'info',
                'text': ann.title,
                'sub': 'Announcement',
                'time': ann.created_at,
            })

        recent.sort(key=lambda x: x['time'], reverse=True)
        recent = recent[:5]

    return {
        'unread_messages': unread,
        'unread_notifications': alerts,
        'activity_dues': dues,
        'activity_recent': recent,
    }
