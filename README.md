# Task Collaboration Tool - Setup & Installation Guide

A complete Django web application for managing tasks collaboratively with Kanban board and list views.

## Features

✅ **User Authentication & Authorization** - Secure login with django-allauth  
✅ **Projects Management** - Create and organize projects  
✅ **Task Management** - Create, assign, and track tasks  
✅ **Dual Views** - Switch between Kanban board and list views  
✅ **Comments & Discussions** - Add comments to tasks for team communication  
✅ **Task Prioritization** - Set priority levels (Low, Medium, High, Urgent)  
✅ **Team Collaboration** - Add team members to projects  
✅ **Responsive Design** - Works on desktop, tablet, and mobile with Tailwind CSS  
✅ **Real-time Drag & Drop** - Drag tasks between Kanban columns  

## Technology Stack

- **Backend**: Django 6.0.6
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: django-allauth

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip
- Virtual environment (venv)

### 2. Clone/Setup Project
```bash
cd collab_tool
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example file
cp .env.example .env

# Edit .env and set your SECRET_KEY (for production)
# For development, defaults are fine
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Enter username, email, password when prompted
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

### Admin Panel
Access Django admin at: **http://localhost:8000/admin/**

## Usage Guide

### Dashboard
- View overview of your projects and tasks
- See statistics (total tasks, assigned tasks, etc.)
- Quick access to recent tasks

### Projects
- **Create Project**: Click "New Project" to create a project
- **Edit Project**: Edit project name, description, and color
- **Add Members**: Invite team members to collaborate
- **Delete Member**: Remove members from the project

### Tasks
- **Create Task**: Add new tasks to a project
- **Assign Task**: Assign tasks to team members
- **Set Priority**: Mark tasks as Low, Medium, High, or Urgent
- **Set Due Date**: Add deadlines for tasks
- **Update Status**: Move tasks between To Do → In Progress → Done

### Views
- **Kanban View**: Drag-and-drop tasks between status columns
- **List View**: View all tasks in a table with sorting and filtering

### Comments
- Add comments to tasks for discussion
- Delete your own comments or comments on your projects (owner only)

### My Tasks
- View all tasks assigned to you
- Filter by status
- Quick actions to mark tasks as done

## File Structure

```
collab_tool/
├── collab_tool/          # Project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py
├── workspace/            # Main app
│   ├── models.py         # Database models (Project, Task, Comment)
│   ├── views.py          # View logic
│   ├── urls.py           # App URL patterns
│   ├── admin.py          # Admin configuration
│   └── migrations/       # Database migrations
├── accounts/             # Authentication app
├── templates/            # HTML templates
│   ├── base.html
│   └── workspace/        # App-specific templates
├── static/               # CSS, JS, images
├── manage.py
├── requirements.txt
└── db.sqlite3           # SQLite database
```

## Models

### Project
- name (CharField)
- description (TextField)
- owner (ForeignKey to User)
- members (ManyToMany Users)
- color (CharField - hex color code)
- created_at, updated_at

### Task
- title (CharField)
- description (TextField)
- project (ForeignKey)
- assigned_to (ForeignKey to User)
- created_by (ForeignKey to User)
- status (todo, in_progress, done)
- priority (low, medium, high, urgent)
- due_date (DateTime)
- order (for Kanban ordering)
- created_at, updated_at

### Comment
- task (ForeignKey)
- author (ForeignKey to User)
- content (TextField)
- created_at, updated_at

## URL Routes

| Route | View | Purpose |
|-------|------|---------|
| `/` | dashboard | Dashboard overview |
| `/projects/` | project_list | All projects |
| `/projects/create/` | project_create | Create new project |
| `/projects/<id>/` | project_detail | Project detail view |
| `/projects/<id>/edit/` | project_edit | Edit project |
| `/projects/<id>/members/` | project_members | Manage members |
| `/projects/<id>/tasks/create/` | task_create | Create task |
| `/tasks/<id>/` | task_detail | Task detail & edit |
| `/tasks/<id>/delete/` | task_delete | Delete task |
| `/tasks/my/` | my_tasks | My assigned tasks |
| `/tasks/<id>/status/` | update_task_status | Update task status (AJAX) |
| `/tasks/<id>/comments/` | add_comment | Add comment (AJAX) |

## API Endpoints (AJAX)

### Update Task Status
```
POST /tasks/<task_id>/status/
Body: { "status": "in_progress", "order": 0 }
```

### Add Comment
```
POST /tasks/<task_id>/comments/
Body: { "content": "Comment text" }
```

## Customization

### Change Colors
Edit the Tailwind color classes in templates. Default colors:
- Blue (primary): `#3B82F6`
- Green (success): `#10B981`
- Red (danger): `#EF4444`
- Yellow (warning): `#F59E0B`

### Add More Task Fields
1. Add field to Task model in `models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Update templates to display the field

### Customize Sidebar
Edit `templates/base.html` to modify navigation menu

## Deployment

### Production Settings
1. Set `DEBUG = False` in settings.py
2. Set secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Set up email backend for notifications
6. Use environment variables for sensitive data
7. Configure static files with WhiteNoise or CDN

### Using PostgreSQL
```bash
pip install psycopg2-binary
```

Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'collab_tool',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Troubleshooting

**Issue**: "No module named 'workspace'"
- Solution: Make sure `workspace` is in INSTALLED_APPS in settings.py

**Issue**: Static files not loading
- Solution: Run `python manage.py collectstatic`

**Issue**: Migration errors
- Solution: Delete migrations folder (except __init__.py), run `python manage.py makemigrations && python manage.py migrate`

**Issue**: Login redirects not working
- Solution: Check LOGIN_REDIRECT_URL in settings.py (should be 'dashboard')

## Support

For issues or questions, check Django documentation: https://docs.djangoproject.com/

## License

This project is open source and available for educational and commercial use.
