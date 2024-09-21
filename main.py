from fasthtml.common import *
from datetime import datetime, timedelta
import calendar
import os
import logging
import yaml
from feedgen.feed import FeedGenerator
from starlette.responses import Response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

styles = Style("""
    .logo-title-container {
        display: flex;
        align-items: center;
        text-decoration: none;
    }
    .custom-logo {
        max-height: 50px;
        margin-right: 10px;
    }
    .calendar-title {
        margin: 0;
    }
    .logo-title-container a {
        text-decoration: none;
    }        .social-button {
            background: none;
            border: none;
            padding: 0.5rem;
            cursor: pointer;
            color: var(--primary);
        }
        .social-button:hover {
            color: var(--primary-hover);
        }
        .social-buttons-container {
            display: flex;
            gap: 0.5rem;
        }
                   .social-button {
        background: none;
        border: none;
        padding: 0.5rem;
        cursor: pointer;
        color: var(--primary);
    }
    .social-button:hover {
        color: var(--primary-hover);
    }
    .social-buttons-container {
        display: flex;
        gap: 0.5rem;
    }
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }
    .powered-by-text {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        text-align: center;
    }
    .powered-by-text a {
        color: var(--primary);
        text-decoration: none;
    }
    .powered-by-text a:hover {
        text-decoration: underline;
    }
""")

def load_custom_settings(filename='custom_settings.yaml'):
    default_settings = {
        "title": "Calendar App",
        "about_content": "This is a calendar application.",
        "website_url": "https://example.com",
        "github_url": "https://github.com/your-repo/path-to-create-pr",
        "social_links": [],
        "default_locations": ["Online", "London"]  # Add this line
    }
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            custom_settings = yaml.safe_load(f)
        default_settings.update(custom_settings)
    return default_settings

custom_settings = load_custom_settings()


custom_settings = load_custom_settings()

app, rt = fast_app(pico=True,
                   hdrs=(
    MarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    Script(src="https://unpkg.com/@phosphor-icons/web"),
    styles
))


db = database('data/calendar.db')
events = db.t.events
if events not in db.t:
    events.create(id=int, title=str, date=str, description=str, url=str, location=str, pk='id')
Event = events.dataclass()


# Replace the load_events_from_json function
def load_events_from_yaml(filename='events.yaml'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    logger.warning(f"Events file {filename} not found.")
    return []

# Update the update_db_from_json function to use YAML
def update_db_from_yaml():
    yaml_events = load_events_from_yaml()
    if not yaml_events:
        logger.warning("No events found in YAML file.")
        return

    for event in yaml_events:
        existing = events(f"title='{event['title']}' AND date='{event['date']}'")
        if not existing:
            try:
                events.insert(Event(**event))
                logger.info(f"Added event: {event['title']} on {event['date']}")
            except Exception as e:
                logger.error(f"Error adding event {event['title']}: {str(e)}")

    # Check if any events were added
    total_events = len(events())
    logger.info(f"Total events in database after update: {total_events}")

# Update the call to this function
update_db_from_yaml()

# Helper functions
def get_month_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    return cal, month_name


def generate_rss_feed():
    fg = FeedGenerator()
    fg.title('Calendar Events')
    fg.description('Upcoming events from our calendar')
    fg.link(href=custom_settings['website_url'])

    upcoming_events = get_upcoming_events(days=30)
    for event in upcoming_events:
        fe = fg.add_entry()
        fe.title(event.title)
        fe.description(event.description)
        fe.link(href=f"{custom_settings['website_url']}/event/{event.id}")
        fe.pubDate(datetime.strptime(event.date, '%Y-%m-%d'))

    return fg.rss_str(pretty=True)


logo_url = "/static/logo.png"
if os.path.exists(f".{logo_url}"):  # Check if the file exists in the static directory
    logo = Img(src=logo_url, cls="custom-logo")
else:
    logo = ""
    logger.error(f"Logo file {logo_url} not found.")

# Create a container for the logo and title
logo_title_container = A(
    logo,
    H1(custom_settings['title'], cls="calendar-title"),
    cls="logo-title-container",
    href="/"  # Link to the home page
)

def create_footer():
    # Add event button (redirects to GitHub)
    add_button = A("Add Event", 
                   href=custom_settings['github_url'], 
                   target="_blank",
                   role="button")

    # About button
    about_button = A("About", href="/about", role="button", cls="outline")

    # Create social buttons
    social_buttons = Div(
        *[A(I(cls=f"ph ph-{link['icon']}"), 
            href=link['url'], 
            target="_blank" if link['url'].startswith('http') else "_self", 
            role="button", 
            cls="social-button",
            title=link['name'])
          for link in custom_settings['social_links']],
        cls="social-buttons-container"
    )

    footer_buttons = Div(add_button, about_button, social_buttons, cls="button-container")

    # Add "Powered by FastCalendar" text
    powered_by = P(
        "Powered by ",
        A("FastCalendar", href="https://github.com/AndreasThinks/FastCalendar", target="_blank"),
        cls="powered-by-text"
    )

    return Div(footer_buttons, powered_by, cls="footer-container")


def get_all_locations():
    return list(set(event.location for event in events()))

def get_events_for_month(year, month, locations=None):
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-31"
    month_events = events(f"date >= '{start_date}' AND date <= '{end_date}'")
    if locations:
        month_events = [e for e in month_events if e.location in locations]
    return month_events

def get_upcoming_events(start_date=None, end_date=None, locations=None):
    if start_date is None:
        start_date = datetime.now().date()
    if end_date is None:
        end_date = start_date + timedelta(days=30)
    
    upcoming = events(f"date >= '{start_date}' AND date <= '{end_date}'")
    if locations:
        upcoming = [e for e in upcoming if e.location in locations]
    return sorted(upcoming, key=lambda e: e.date)  # Sort events by date

def show_main_layout(year, month, active_locations, view='calendar', event_id=None):
    if event_id:
        event = events[event_id]
        return Titled(
            event.title,
            Div(
                H3(event.title),
                P(f"Date: {event.date}"),
                P(f"Location: {event.location}"),
                P(event.description),
                A("Back to Calendar", href=f"/calendar_content/{year}/{month}?locations={'+'.join(active_locations)}&view={view}", role="button", cls="outline")
            )
        )

    all_locations = get_all_locations()
    
    # Location filter buttons
    location_filters = Div(
        *[A(location, 
            href=f"/toggle_location/{year}/{month}/{location}?locations={'+'.join(active_locations)}&view={view}",
            role="button",
            cls=f"{'active' if location in active_locations else 'outline'} location-filter")
          for location in all_locations],
        cls="location-filters"
    )

    nav = Div(
        A("< Prev", href=f"/calendar_content/{year}/{month}?direction=prev&locations={'+'.join(active_locations)}&view={view}", role="button", cls="outline"),
        H2(f"{calendar.month_name[month]} {year}", id="current-month-year"),
        A("Next >", href=f"/calendar_content/{year}/{month}?direction=next&locations={'+'.join(active_locations)}&view={view}", role="button", cls="outline"),
        cls="calendar-nav"
    )
    
    view_toggle = Div(
        A("Calendar", href=f"/calendar_content/{year}/{month}?view=calendar&locations={'+'.join(active_locations)}", role="button", cls="active" if view == 'calendar' else "outline"),
        A("Agenda", href=f"/calendar_content/{year}/{month}?view=agenda&locations={'+'.join(active_locations)}", role="button", cls="active" if view == 'agenda' else "outline"),
        cls="view-toggle"
    )

    header = Div(
        nav,
        view_toggle,
        location_filters,
    )

    cal, _ = get_month_calendar(year, month)
    month_events = get_events_for_month(year, month, active_locations)
    content = get_calendar_content(year, month, view, cal, month_events, active_locations)

    calendar_container = Div(
        logo_title_container,  # Add logo and title container here
        header,
        content,
        create_footer(),
        id="calendar-container"
    )
    
    event_dialog = Container(
        Div(id="event-dialog-content"),
        header=Div(Button("×", aria_label="Close", _="on click hide #event-dialog")),
        footer=Div(Button("Close", cls="secondary", _="on click hide #event-dialog")),
        id="event-dialog"
    )

    about_dialog = Container(
        Div(id="about-dialog-content", cls="marked"),
        header=Div(Button("×", aria_label="Close", _="on click hide #about-dialog")),
        footer=Div(Button("Close", cls="secondary", _="on click hide #about-dialog")),
        id="about-dialog"
    )

    return (Title(custom_settings['title']),
            Container(
            Style("""
                .calendar-nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
                .calendar-nav h2 { margin: 0; }
                .view-toggle { display: flex; justify-content: center; gap: 10px; margin-bottom: 1rem; }
                .calendar-table { width: 100%; table-layout: fixed; }
                .calendar-table th { text-align: center; font-weight: bold; }
                .calendar-cell { height: 100px; vertical-align: top; padding: 5px !important; }
                .day-number { font-weight: bold; margin-bottom: 5px; }
                .event-link { display: block; margin-bottom: 2px; font-size: 0.8em; }
                .agenda-list { list-style-type: none; padding: 0; }
                .agenda-list li { margin-bottom: 1rem; }
                .button-container { display: flex; justify-content: space-between; margin-top: 1rem; }
                .logo-container { display: flex; justify-content: center; margin-bottom: 1rem; }
                .custom-logo { max-height: 50px; margin-right: 10px; }
                .logo-title-container { display: flex; align-items: center; margin-bottom: 1rem; }
                .calendar-title { margin: 0; }
                #about-dialog-content { padding: 1rem; }
                .location-filter { font-size: 0.8rem; padding: 0.2rem 0.5rem; border-radius: 1rem; }
                .location-filter.active { background-color: var(--primary); color: var(--primary-inverse); }
                .button-container { display: flex; justify-content: space-between; margin-top: 1rem; }
            """),
            calendar_container,
            event_dialog,
            about_dialog
        ))

@rt("/")
def get(req):
    today = datetime.now()
    default_locations = '+'.join(custom_settings.get('default_locations', ['Online', 'London']))
    active_locations = set(req.query_params.get('locations', default_locations).replace('+', ' ').split())
    view = req.query_params.get('view', 'calendar')
    return (Title(custom_settings['title']), Container(show_main_layout(today.year, today.month, active_locations, view)))


@rt("/rss")
def get():
    rss_feed = generate_rss_feed()
    return Response(content=rss_feed, media_type="application/rss+xml")

@rt("/about")
def get():
    return (Title('About ' + custom_settings['title']), 
             Container(
        logo_title_container,
        Div(custom_settings['about_content'], cls="marked"),  # Add the "marked" class to render as Markdown
        create_footer()
    ))

@rt("/calendar_content/{year}/{month}")
def get(year: int, month: int, view: str = 'calendar', direction: str = None, locations: str = None):
    if locations is None:
        default_locations = '+'.join(custom_settings.get('default_locations', ['Online', 'London']))
        locations = default_locations
    active_locations = set(locations.replace('+', ' ').split())
    if direction == 'prev':
        date = datetime(year, month, 1) - timedelta(days=1)
        year, month = date.year, date.month
    elif direction == 'next':
        date = datetime(year, month, 1) + timedelta(days=32)
        year, month = date.year, date.month

    return show_main_layout(year, month, active_locations, view)

# Update the toggle_location route to use the default locations from settings
@rt("/toggle_location/{year}/{month}/{location}")
def get(year: int, month: int, location: str, locations: str = None, view: str = 'calendar'):
    if locations is None:
        default_locations = '+'.join(custom_settings.get('default_locations', ['Online', 'London']))
        locations = default_locations
    active_locations = set(locations.replace('+', ' ').split())
    if location in active_locations:
        active_locations.remove(location)
    else:
        active_locations.add(location)
    
    new_locations = '+'.join(sorted(active_locations))  # Sort for consistency
    return RedirectResponse(url=f"/calendar_content/{year}/{month}?locations={new_locations}&view={view}", status_code=303)


def get_calendar_content(year, month, view, cal, month_events, active_locations):
    if view == 'calendar':
        weekdays = [calendar.day_abbr[i] for i in range(7)]
        weekday_headers = [Th(day) for day in weekdays]
        
        calendar_body = []
        for week in cal:
            week_row = []
            for day in week:
                if day == 0:
                    week_row.append(Td(""))
                else:
                    day_events = [e for e in month_events if e.date == f"{year}-{month:02d}-{day:02d}"]
                    day_content = [
                        Div(str(day), cls="day-number"),
                        *[A(f"{e.title} ({e.location})", 
                            href=f"/event/{e.id}",
                            cls="event-link"
                          ) for e in day_events if e.location in active_locations]
                    ]
                    week_row.append(Td(*day_content, cls="calendar-cell"))
            calendar_body.append(Tr(*week_row))
        
        return Table(
            Thead(Tr(*weekday_headers)),
            Tbody(*calendar_body),
            cls="calendar-table"
        )
    else:  # Agenda view
        start_date = datetime(year, month, 1).date()
        end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        upcoming_events = get_upcoming_events(start_date=start_date, end_date=end_date, locations=active_locations)
        return Ul(*[
            Li(
                H4(e.date),
                A(f"{e.title} ({e.location})", 
                  href=f"/event/{e.id}")
            ) for e in upcoming_events
        ], cls="agenda-list")

@rt("/event/{id}")
def get(id: int):
    event = events[id]
    event_url = A("Event Link", href=event.url, target="_blank") if event.url else ""
    return (Title(event.title),
            Container(
        logo_title_container,
        Article(
            H3(event.title),
            P(f"Date: {event.date}"),
            P(f"Location: {event.location}"),
            Div(event.description, cls="marked"),  # Add the "marked" class to render as Markdown
            event_url
        ),
        create_footer()
    ))



serve()
