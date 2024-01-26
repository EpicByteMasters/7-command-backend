"""empty message

Revision ID: 6d8611e1f400
Revises: 
Create Date: 2024-01-25 22:41:31.902812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d8611e1f400'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competency',
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('skill_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goal',
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('position',
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialty',
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status',
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taskfile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('url_link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taskstatus',
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competencyspecialty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('specialty', sa.String(), nullable=True),
    sa.Column('competency', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['competency'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['specialty'], ['specialty.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('education',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('specialty', sa.String(), nullable=True),
    sa.Column('url_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['specialty'], ['specialty.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('patronymic', sa.String(length=64), nullable=True),
    sa.Column('position_id', sa.Integer(), nullable=True),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('supervisor_id', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['position_id'], ['position.id'], ),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialty.id'], ),
    sa.ForeignKeyConstraint(['supervisor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('competencyeducation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('competency', sa.String(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competency'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ipr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('supervisor_id', sa.Integer(), nullable=False),
    sa.Column('goal', sa.String(), nullable=True),
    sa.Column('specialty', sa.String(), nullable=True),
    sa.Column('create_date', sa.Date(), nullable=True),
    sa.Column('close_date', sa.Date(), nullable=True),
    sa.Column('mentor_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('ipr_status', sa.String(), nullable=False),
    sa.Column('ipr_grade', sa.Integer(), nullable=True),
    sa.Column('supervisor_comment', sa.Text(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0'), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['goal'], ['goal.id'], ),
    sa.ForeignKeyConstraint(['ipr_status'], ['status.id'], ),
    sa.ForeignKeyConstraint(['mentor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['specialty'], ['specialty.id'], ),
    sa.ForeignKeyConstraint(['supervisor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(length=256), nullable=True),
    sa.Column('briefText', sa.Text(length=256), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialtyeducation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('specialty', sa.String(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['specialty'], ['specialty.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competencyipr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('competency', sa.String(), nullable=True),
    sa.Column('ipr_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competency'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ipr_id'], ['ipr.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('close_date', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('supervisor_comment', sa.Text(), nullable=True),
    sa.Column('task_status', sa.String(), nullable=True),
    sa.Column('file', sa.Integer(), nullable=True),
    sa.Column('ipr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['file'], ['taskfile.id'], ),
    sa.ForeignKeyConstraint(['ipr_id'], ['ipr.id'], ),
    sa.ForeignKeyConstraint(['task_status'], ['taskstatus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('educationtask',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), server_default=sa.text('0'), nullable=True),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('educationtask')
    op.drop_table('task')
    op.drop_table('competencyipr')
    op.drop_table('specialtyeducation')
    op.drop_table('notification')
    op.drop_table('ipr')
    op.drop_table('competencyeducation')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('education')
    op.drop_table('competencyspecialty')
    op.drop_table('taskstatus')
    op.drop_table('taskfile')
    op.drop_table('status')
    op.drop_table('specialty')
    op.drop_table('position')
    op.drop_table('goal')
    op.drop_table('competency')
    # ### end Alembic commands ###