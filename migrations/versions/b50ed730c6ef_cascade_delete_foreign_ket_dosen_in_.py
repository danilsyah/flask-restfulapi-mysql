"""cascade delete foreign ket dosen in mahasiswa

Revision ID: b50ed730c6ef
Revises: 120d7ab4ce9c
Create Date: 2022-04-10 05:38:19.022547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b50ed730c6ef'
down_revision = '120d7ab4ce9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mahasiswa_ibfk_2', 'mahasiswa', type_='foreignkey')
    op.drop_constraint('mahasiswa_ibfk_1', 'mahasiswa', type_='foreignkey')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_satu'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_dua'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.create_foreign_key('mahasiswa_ibfk_1', 'mahasiswa', 'dosen', ['dosen_dua'], ['id'])
    op.create_foreign_key('mahasiswa_ibfk_2', 'mahasiswa', 'dosen', ['dosen_satu'], ['id'])
    # ### end Alembic commands ###