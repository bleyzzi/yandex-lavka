"""create db

Revision ID: e1fcfea4b780
Revises: 
Create Date: 2023-04-29 12:27:22.287054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1fcfea4b780'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courier_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
        sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
        sa.Column('Weight', sa.Float(), nullable=True),
        sa.Column('Region', sa.Integer(), nullable=True),
        sa.Column('Delivery_time', sa.String(), nullable=True),
        sa.Column('Cost', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courier',
        sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
        sa.Column('Courier_type', sa.Integer(), nullable=True),
        sa.Column('Regions', sa.JSON(), nullable=True),
        sa.Column('Working_hours', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['Courier_type'], ['courier_type.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('confirm_order',
        sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
        sa.Column('Courier_id', sa.Integer(), nullable=True),
        sa.Column('Order_id', sa.Integer(), nullable=True),
        sa.Column('Status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['Courier_id'], ['courier.id'], ),
        sa.ForeignKeyConstraint(['Order_id'], ['order.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('confirm_order')
    op.drop_table('courier')
    op.drop_table('order')
    op.drop_table('courier_type')
    # ### end Alembic commands ###
