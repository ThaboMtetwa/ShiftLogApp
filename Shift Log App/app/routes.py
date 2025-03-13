import csv
import os
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.db import session
from app.models import Worker, Shift, PAY_TIERS


def index():
    workers = session.query(Worker).all()
    print("Current workers:", [(w.id, w.first_name, w.last_name) for w in workers])
    selected_worker = None
    worker_shifts = None
    worker_id = request.args.get('worker_id')
    if worker_id and worker_id.strip():
        selected_worker = session.query(Worker).get(worker_id)
        if selected_worker:
            worker_shifts = session.query(Shift).filter_by(worker_id=selected_worker.id).all()

    return render_template('index.html',
                           workers=workers,
                           selected_worker=selected_worker,
                           worker_shifts=worker_shifts)


def add_worker():
    if request.method == 'POST':
        print("Form data received:", request.form)
        employee_number = request.form.get('employee_number')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        pay_tier = request.form.get('pay_tier')

        # Validate and add worker to the database
        if employee_number and first_name and last_name and pay_tier:
            try:
                worker = Worker(
                    employee_number=int(employee_number),
                    first_name=first_name,
                    last_name=last_name,
                    pay_tier=int(pay_tier)
                )
                session.add(worker)
                session.commit()
                flash(f'Worker {first_name} {last_name} added successfully.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                session.rollback()
                flash(f'An error occurred while adding the worker: {e}', 'danger')
        else:
            flash('All fields are required.', 'danger')

    return render_template('add_worker.html', PAY_TIERS=PAY_TIERS)


def add_shift(worker_id):
    if worker_id == 0:
        flash("Please select a worker.", "warning")
        return redirect(url_for('index'))

    worker = session.query(Worker).get(worker_id)
    if not worker:
        flash('Worker not found.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')

        # Parse the start and end times
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')
            shift = Shift(worker=worker, start_time=start_time, end_time=end_time)
            shift.calculate_hours_worked()
            shift.calculate_pay()
            session.add(shift)
            session.commit()
            flash('Shift logged successfully.', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid time format. Please use HH:MM.', 'danger')

    return render_template('add_shift.html', worker=worker)


def export_workers_csv():
    workers = session.query(Worker).all()
    file_path = os.path.join('static', 'workers.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Employee Number', 'First Name', 'Last Name', 'Pay Tier'])
        for worker in workers:
            writer.writerow([worker.employee_number, worker.first_name, worker.last_name, worker.pay_tier])

    flash(f"Worker data has been exported to {file_path}.", 'success')
    return send_from_directory(directory='static', path='workers.csv')


def export_shifts_csv():
    shifts = session.query(Shift).all()
    file_path = os.path.join('static', 'shifts.csv')  # Save to static directory

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Worker ID', 'Date', 'Start Time', 'End Time', 'Hours Worked', 'Pay Earned'])
        for shift in shifts:
            writer.writerow(
                [shift.worker_id, shift.date, shift.start_time, shift.end_time, shift.hours_worked, shift.pay_earned])

    flash(f"Shift data has been exported to {file_path}.", 'success')
    return send_from_directory(directory='static', path='shifts.csv')


def shift_results(shift_id):
    shift = session.query(Shift).get(shift_id)
    if not shift:
        flash('Shift not found.', 'danger')
        return redirect(url_for('index'))
    return render_template('shift_results.html', shift=shift)


# Export a Worker's Shifts
def export_worker_shifts_csv(worker_id):
    from flask import current_app  # Import current_app within the function
    # Ensure the worker exists
    worker = session.query(Worker).get(worker_id)
    if not worker:
        flash("Worker not found.", "danger")
        return redirect(url_for('index'))

    # Query only the shifts for this worker
    worker_shifts = session.query(Shift).filter_by(worker_id=worker.id).all()

    # Get the absolute path of the static folder (e.g., app/static)
    static_folder = current_app.static_folder
    # Define a unique CSV file path for this worker
    file_path = os.path.join(static_folder, f'worker_{worker_id}_shifts.csv')

    # Write the worker's shifts to the CSV file, now including the worker's name in the table
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header row with added "Worker Name" column
        writer.writerow(['Worker ID', 'Worker Name', 'Date', 'Start Time', 'End Time', 'Hours Worked', 'Pay Earned'])
        for shift in worker_shifts:
            writer.writerow([
                shift.worker_id,
                f"{worker.first_name} {worker.last_name}",
                shift.date,
                shift.start_time,
                shift.end_time,
                shift.hours_worked,
                shift.pay_earned
            ])

    flash(f"Shift data for {worker.first_name} {worker.last_name} has been exported.", 'success')
    # Force download by setting as_attachment=True, using the absolute static folder path
    return send_from_directory(
        directory=static_folder,
        path=f'worker_{worker_id}_shifts.csv',
        as_attachment=True
    )
