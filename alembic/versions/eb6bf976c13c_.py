"""empty message

Revision ID: eb6bf976c13c
Revises: 5037819e1654
Create Date: 2024-01-21 00:01:58.973260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb6bf976c13c'
down_revision = '5037819e1654'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taskfile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('url_link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taskstatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competencyspecialty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('competency_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competency_id'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialty.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('education',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('competency_id', sa.Integer(), nullable=True),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('url_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['competency_id'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialty.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('supervisor_comment', sa.Text(), nullable=True),
    sa.Column('task_status_id', sa.Integer(), nullable=True),
    sa.Column('file', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file'], ['taskfile.id'], ),
    sa.ForeignKeyConstraint(['task_status_id'], ['taskstatus.id'], ),
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
    op.create_table('competencylearning',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('competency_id', sa.Integer(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competency_id'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
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
    op.create_table('ipr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emplyee_id', sa.Integer(), nullable=False),
    sa.Column('supervisor_id', sa.Integer(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('mentor_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('ipr_status_id', sa.Integer(), nullable=False),
    sa.Column('ipr_grade_id', sa.Integer(), nullable=True),
    sa.Column('supervisor_comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['emplyee_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['goal_id'], ['goal.id'], ),
    sa.ForeignKeyConstraint(['ipr_grade_id'], ['grade.id'], ),
    sa.ForeignKeyConstraint(['ipr_status_id'], ['status.id'], ),
    sa.ForeignKeyConstraint(['mentor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialty.id'], ),
    sa.ForeignKeyConstraint(['supervisor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialtyeducation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialty.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competencyipr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('competency_id', sa.Integer(), nullable=True),
    sa.Column('idr_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competency_id'], ['competency.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idr_id'], ['ipr.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taskipr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ipr_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ipr_id'], ['ipr.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('taskipr')
    op.drop_table('competencyipr')
    op.drop_table('specialtyeducation')
    op.drop_table('ipr')
    op.drop_table('educationtask')
    op.drop_table('competencylearning')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('task')
    op.drop_table('education')
    op.drop_table('competencyspecialty')
    op.drop_table('taskstatus')
    op.drop_table('taskfile')
    op.drop_table('status')
    op.drop_table('specialty')
    op.drop_table('position')
    op.drop_table('grade')
    op.drop_table('goal')
    op.drop_table('competency')
    # ### end Alembic commands ###
