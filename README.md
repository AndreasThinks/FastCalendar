# FastCalendar

This is a web-based calendar application built with FastHTML, providing an interactive and customizable event viewing experience.

It is primarily intended to be deployed directly from a Github repository, allowing event submission via PR.

## Features

- Interactive calendar view with month navigation
- Agenda view for upcoming events
- Location-based event filtering
- RSS feed for event subscriptions
- Customizable title and about section
- Social media links integration
- Static logo display
- Markdown support for event descriptions and about section

## Prerequisites

- Python 3.11+
- uv

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/awesome-calendar.git
   cd awesome-calendar
   ```

2. Create and activate a virtual environment:
   ```
   uv init
   ```

3. Install the required packages:
   ```
   uv sync
   ```

4. Create a `custom_settings.yaml` file in the project root with the following structure:
   ```yaml
   title: My Awesome Calendar
   about_content: |
     # About

     This is my awesome calendar application.

     ## Features
     - Easy to use
     - Customizable
     - Markdown support
   website_url: https://example.com
   github_url: https://github.com/your-username/awesome-calendar
   default_locations:
     - Online
     - London
   social_links:
     - name: RSS
       url: /rss
       icon: rss-simple
     - name: Discord
       url: https://discord.gg/your-server
       icon: discord-logo
   ```

5. Create an `events.yaml` file in the project root to populate your calendar with events:
   ```yaml
   - id: 1
     title: Team Meeting
     date: 2024-09-15
     description: |
       # Weekly Team Sync-up

       ## Agenda
       - Project updates
       - Upcoming deadlines
       - Q&A session

       Join us at [Google Meet](https://meet.google.com/abc-defg-hij)
     url: https://meet.google.com/abc-defg-hij
     location: Online

   - id: 2
     title: Project Deadline
     date: 2024-09-30
     description: |
       **Final submission for Q3 project**

       Make sure to:
       - Complete all deliverables
       - Review documentation
       - Prepare presentation slides
     url: ""
     location: London
   ```

6. Add your logo image file (e.g., `logo.png`) to the `static` folder in the project root.

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5001` (or the port specified in your configuration).

3. Use the calendar view to browse events, switch to the agenda view, or filter events by location.

4. Click on events to view details. Event descriptions support Markdown formatting.

5. Use the social media buttons in the footer to access linked platforms or subscribe to the RSS feed.

## Customization

- Modify the `custom_settings.yaml` file to change the application title, about content, website URL, GitHub URL, default locations, and social media links.
- Edit the `events.yaml` file to add, remove, or modify events. Event descriptions support Markdown formatting.
- Replace the `logo.png` file in the `static` folder to change the application logo.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.