import logging
import logging.config
import json
import argparse
import os

# Configure logging
logging.config.fileConfig('task_tracker.ini')
logger = logging.getLogger(__name__)

JSON_FILE = 'tasks.JSON'

def load_tasks():
    if not os.path.exists(JSON_FILE):
        logger.info("Task file does not exist. Creating a new one.")
        return {"tasks": []}
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from file {JSON_FILE}: {e}")
        return {"tasks": []}
    except IOError as e:
        logger.error(f"IO error occurred while reading {JSON_FILE}: {e}")
        return {"tasks": []}
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return {"tasks": []}

def save_tasks(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        logger.info("Tasks saved to file.")

def add_task(title, description):
    data = load_tasks()
    new_id = max([task['id'] for task in data['tasks']], default=0) + 1
    new_task = {"id": new_id, "title": title, "description": description, "status": "not done"}
    data['tasks'].append(new_task)
    save_tasks(data)

def update_task(task_id, title=None, description=None, status=None):
    data = load_tasks()
    task_found = False
    for task in data['tasks']:
        if task['id'] == task_id:
            if title is not None:
                task['title'] = title
            if description is not None:
                task['description'] = description
            if status is not None:
                task['status'] = status
            task_found = True
            break
    save_tasks(data)
    if task_found:
        logger.info(f"Task {task_id} updated. Title: '{title}', Description: '{description}', Status: '{status}'")
    else:
        logger.warning(f"Task {task_id} not found for update.")

def delete_task(task_id):
    data = load_tasks()
    data['tasks'] = [task for task in data['tasks'] if task['id'] != task_id]
    save_tasks(data)
    logger.info(f"Task {task_id} deleted.")

def list_tasks(status=None):
    data = load_tasks()
    tasks = data['tasks']
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    for task in tasks:
        print(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}, Status: {task['status']}")
    logger.info(f"Listed tasks. Filtered by status: '{status}'" if status else "Listed all tasks.")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Add task
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('title', type=str, help='Task title')
    add_parser.add_argument('description', type=str, help='Task description')

    # Update task
    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument('--title', type=str, help='New task title')
    update_parser.add_argument('--description', type=str, help='New task description')
    update_parser.add_argument('--status', type=str, choices=['not done', 'in progress', 'done'], help='New task status')

    # Delete task
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('id', type=int, help='Task ID')

    # List tasks
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--status', type=str, choices=['not done', 'in progress', 'done'], help='Filter tasks by status')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.title, args.description)
    elif args.command == 'update':
        update_task(args.id, args.title, args.description, args.status)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'list':
        list_tasks(args.status)

if __name__ == '__main__':
    main()