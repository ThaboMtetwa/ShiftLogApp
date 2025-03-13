
engine = create_engine('sqlite:///shift_management.db')
Session = sessionmaker(bind=engine)
session = Session()

def view_workers():
    workers = session.query(Worker).all()
    print("Workers in the database:")
    for worker in workers:
        print(worker)

def view_shifts():
    shifts = session.query(Shift).all()
    print("Shifts in the database:")
    for shift in shifts:
        print(shift)

if __name__ == '__main__':
    view_workers()
    view_shifts()