from app.db import Base
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# Pay tier dictionary
PAY_TIERS = {
    1: 15.00,
    2: 20.00,
    3: 25.00,
    4: 30.00,
    5: 40.00,
}


class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    employee_number = Column(Integer, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    pay_tier = Column(Integer, nullable=False)

    # Establish relationship with Shift model
    shifts = relationship('Shift', back_populates='worker')

    def __init__(self, employee_number, first_name, last_name, pay_tier):
        self.employee_number = employee_number
        self.first_name = first_name
        self.last_name = last_name
        self.pay_tier = pay_tier

    def __repr__(self):
        return f'<Worker {self.first_name} {self.last_name}, Pay Tier: {self.pay_tier}>'


class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    hours_worked = Column(Float, default=0)
    pay_earned = Column(Float, default=0)

    # Relationship to Worker model
    worker = relationship('Worker', back_populates='shifts')

    def __init__(self, worker, start_time=None, end_time=None):
        self.worker = worker
        self.date = datetime.now().date()
        self.start_time = start_time
        self.end_time = end_time
        self.hours_worked = 0
        self.pay_earned = 0

    def calculate_hours_worked(self):
        if self.start_time and self.end_time:
            time_diff = self.end_time - self.start_time
            self.hours_worked = time_diff.total_seconds() / 3600  # Convert seconds to hours

    def calculate_pay(self):
        if self.hours_worked > 0:
            pay_rate = PAY_TIERS.get(self.worker.pay_tier, 0)
            self.pay_earned = self.hours_worked * pay_rate

    def __repr__(self):
        return (f'<Shift Date: {self.date}, Hours Worked: {self.hours_worked}, '
                f'Pay Earned: ${self.pay_earned:.2f}>')
