import uuid
from gino import Gino
from sqlalchemy.dialects.postgresql import UUID
from config import BIND

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(), default=uuid.uuid4(), primary_key=True)
    name = db.Column(db.Unicode(length=128,), index=True)
    account = db.Column(db.DECIMAL(12, 2), default=0)
    hold = db.Column(db.DECIMAL(12, 2), default=0)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return (f'id: {self.id}, name: {self.name}, account: {self.account}, '
                f'hold: {self.hold}, status: {self.status}')


async def create_init():
    users = [
        User(id=uuid.UUID('26c940a1-7228-4ea2-a3bc-e6460b172040'),
             name='Петров Иван Сергеевич',
             account=1700,
             hold=300,
             status=True),

        User(id=uuid.UUID('7badc8f8-65bc-449a-8cde-855234ac63e1'),
             name='Kazitsky Jason',
             account=200,
             hold=200,
             status=True),

        User(id=uuid.UUID('5597cc3d-c948-48a0-b711-393edf20d9c0'),
             name='Пархоменко Антон Александрович',
             account=10,
             hold=300,
             status=True),

        User(id=uuid.UUID('867f0924-a917-4711-939b-90b179a96392'),
             name='Петечкин Петр Измаилович',
             account=1000000,
             hold=1,
             status=False),
    ]
    for user in users:
        print(f'Creating {user} ...')
        try:
            await user.create()
        except Exception as e:
            print(str(e))
