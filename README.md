# Support Ticketing System

A text-based technical support ticketing application built using Python and MongoDB, where issue types are organized into categories.

## Features

- Load categories and issue types from an external file.
- Create, view, and update tickets.
- Search tickets by category and status.
- Predefined status options for tickets: Open, Pending, Closed.
- Cleanup of orphaned tickets (tickets with non-existent categories).

## Requirements

- Python 3.x
- pymongo
- MongoDB

## Setup

### MongoDB

Ensure you have MongoDB installed and running locally. If you need to install MongoDB, you can follow the instructions [here](https://docs.mongodb.com/manual/installation/).

### Python

1. Clone this repository:
   ```bash
   git clone https://github.com/AdhamAfis/support-ticket-app.git
   cd support-ticket-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### External File

Ensure you have a `categories.txt` file in the same directory as the script. The file should be formatted as follows:

```
Category1:
  IssueType1
  IssueType2
Category2:
  IssueType1
  IssueType2
...
```

### Example `categories.txt`

```
Hardware:
  Printer not working
  Monitor flickering
  Keyboard not responding
Software:
  Unable to install software
  Application crashes
  Password reset required
```

## Usage

Run the application:

```bash
python support_ticket_app.py
```

Follow the on-screen prompts to interact with the application.

### Main Menu Options

1. **Create a new ticket**: Choose a category, select an issue type, and provide a description.
2. **View all tickets**: Display all tickets with their details and categories.
3. **Update ticket status**: Enter the ticket ID and choose a new status (Open, Pending, Closed).
4. **Search tickets by category**: Enter a category name to view all related tickets.
5. **Search tickets by status**: Enter a status to view all tickets with that status.
6. **Exit**: Exit the application.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for review.
