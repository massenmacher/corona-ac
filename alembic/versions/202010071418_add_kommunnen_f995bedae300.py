"""Add Kommunnen

Revision ID: f995bedae300
Revises: 
Create Date: 2020-10-07 14:18:51.127277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f995bedae300'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'cases_ac', 
        sa.Column('alsdorf', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('baesweiler', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('eschweiler', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('herzogenrath', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('monschau', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('roetgen', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('simmerath', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('stolberg', sa.Integer)
    )
    op.add_column(
        'cases_ac', 
        sa.Column('wuerselen', sa.Integer)
    )


def downgrade():
    op.drop_column(
        'cases_ac', 
        sa.Column('alsdorf', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('baesweiler', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('eschweiler', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('herzogenrath', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('monschau', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('roetgen', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('simmerath', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('stolberg', sa.Integer)
    )
    op.drop_column(
        'cases_ac', 
        sa.Column('wuerselen', sa.Integer)
    )

