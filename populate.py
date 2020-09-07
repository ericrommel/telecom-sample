import string
from random import choice

from app import db
from app.models import Employee, DidNumber


def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    a_string = "".join(choice(letters) for i in range(length))
    return a_string


def get_random_int(length: int) -> int:
    if length > 10:
        length = 10

    numbers = "0123456789"
    a_string = "".join(choice(numbers) for i in range(length))
    return int(a_string)


db.create_all()

for i in range(10):
    username = get_random_string(10)
    email = f"{username}@gmail.com"
    employee = Employee(
        username=username,
        password="123456",
        is_admin=False,
        first_name="First Name",
        last_name="Last Name",
        email=email,
    )

    number = f"+55 {get_random_int(2)} {get_random_int(4)-get_random_int(4)}"
    did_number = DidNumber(
        value=number,
        monthly_price="0.06",
        setup_price="3.49",
        currency="U$",
    )
    print(employee)
    print(did_number)
    # save users to database
    try:
        db.session.add(employee)
        db.session.add(did_number)
        db.session.commit()
    except Exception as e:
        print(e)
