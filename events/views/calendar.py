# events/services/calendar.py

from uuid import uuid4
from urllib.parse import quote

from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone


class EventCalendarService:

    @staticmethod
    def to_utc(dt):
        """
        Ensure datetime is UTC.
        """

        if timezone.is_naive(dt):
            dt = timezone.make_aware(
                dt,
                timezone.get_current_timezone()
            )

        return dt.astimezone(
            timezone.utc
        )

    @staticmethod
    def calendar_datetime(dt):
        """
        Calendar format:
        20260715T180000Z
        """

        dt = EventCalendarService.to_utc(dt)

        return dt.strftime(
            "%Y%m%dT%H%M%SZ"
        )

    @staticmethod
    def google_url(event):

        start = EventCalendarService.calendar_datetime(
            event.event_startdate
        )

        end = EventCalendarService.calendar_datetime(
            event.event_enddate
        )

        return (
            "https://calendar.google.com/calendar/render"
            "?action=TEMPLATE"
            f"&text={quote(event.title)}"
            f"&dates={start}/{end}"
            f"&details={quote(event.description or '')}"
            f"&location={quote(event.venue_name or '')}"
        )

    @staticmethod
    def outlook_url(event):

        start = EventCalendarService.to_utc(
            event.event_startdate
        ).isoformat()

        end = EventCalendarService.to_utc(
            event.event_enddate
        ).isoformat()

        return (
            "https://outlook.live.com/calendar/0/deeplink/compose"
            f"?subject={quote(event.title)}"
            f"&body={quote(event.description or '')}"
            f"&location={quote(event.venue_name or '')}"
            f"&startdt={quote(start)}"
            f"&enddt={quote(end)}"
        )

    @staticmethod
    def apple_url(request, event):
        """
        Apple uses ICS downloads.
        """

        return request.build_absolute_uri(
            reverse(
                "apple_calendar_download",
                kwargs={
                    "event_id": event.id
                }
            )
        )

    @staticmethod
    def generate_ics(event):

        start = EventCalendarService.calendar_datetime(
            event.event_startdate
        )

        end = EventCalendarService.calendar_datetime(
            event.event_enddate
        )

        uid = f"{uuid4()}@bbgi.co.za"

        description = (
            event.description or ""
        ).replace("\n", "\\n")

        location = (
            event.venue_name or ""
        )

        return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//BBGI//Events//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
SUMMARY:{event.title}
DESCRIPTION:{description}
LOCATION:{location}
DTSTART:{start}
DTEND:{end}
STATUS:CONFIRMED
SEQUENCE:0
TRANSP:OPAQUE
END:VEVENT
END:VCALENDAR
"""

    @staticmethod
    def apple_download_response(event):

        response = HttpResponse(
            EventCalendarService.generate_ics(
                event
            ),
            content_type="text/calendar"
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; filename="{event.slug}.ics"'
        )

        return response

    @staticmethod
    def get_links(request, event):

        return {
            "google_calendar_url":
                EventCalendarService.google_url(
                    event
                ),

            "outlook_calendar_url":
                EventCalendarService.outlook_url(
                    event
                ),

            "apple_calendar_url":
                EventCalendarService.apple_url(
                    request,
                    event
                )
        } 