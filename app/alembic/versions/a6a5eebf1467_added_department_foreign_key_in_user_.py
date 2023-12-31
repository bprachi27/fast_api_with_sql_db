"""added department foreign key in user table

Revision ID: a6a5eebf1467
Revises: dcc2ccd8f81e
Create Date: 2023-10-02 12:31:41.051088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6a5eebf1467'
down_revision: Union[str, None] = 'dcc2ccd8f81e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('my_department_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'department', ['my_department_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'my_department_id')
    # ### end Alembic commands ###
