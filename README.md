# Awesome Calendar Application

This is a web-based calendar application built with FastHTML, providing an interactive and customizable event viewing experience.

## Features

- Interactive calendar view with month navigation
- Agenda view for upcoming events
- Location-based event filtering
- RSS feed for event subscriptions
- Customizable title and logo
- About section with markdown support

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

4. Create a `custom_settings.json` file in the project root with the following structure:
   ```json
   {
     "title": "My Awesome Calendar",
     "logo_url": "/path/to/your/logo.png",
     "about_content": "# About\n\nThis is my awesome calendar application."
   }
   ```

5. Create an `events.json` file in the project root to populate your calendar with events:
   ```json
   [
     {
       "id": 1,
       "title": "Team Meeting",
       "date": "2024-09-15",
       "description": "Weekly team sync-up",
       "url": "https://meet.google.com/abc-defg-hij",
       "location": "Online"
     },
     {
       "id": 2,
       "title": "Project Deadline",
       "date": "2024-09-30",
       "description": "Final submission for Q3 project",
       "url": "",
       "location": "London"
     }
   ]
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5001` (or the port specified in your configuration).

3. Use the calendar view to browse events, switch to the agenda view, or filter events by location.

4. Click on events to view details.

5. Use the RSS feed button to subscribe to upcoming events.

## Customization

- Modify the `custom_settings.json` file to change the application title, logo, and about content.
- Edit the `events.json` file to add, remove, or modify events.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.