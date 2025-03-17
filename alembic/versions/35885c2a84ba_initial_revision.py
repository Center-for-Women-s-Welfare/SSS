"""initial revision

Revision ID: 35885c2a84ba
Revises:
Create Date: 2023-04-07 13:29:22.075064

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "35885c2a84ba"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "arpa",
        sa.Column("family_type", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("analysis_type", sa.String(), nullable=False),
        sa.Column("federal_and_oregon_eitc", sa.Float(), nullable=True),
        sa.Column("federal_cdctc", sa.Float(), nullable=True),
        sa.Column("federal_income_taxes", sa.Float(), nullable=True),
        sa.Column("payroll_taxes", sa.Float(), nullable=True),
        sa.Column("state_income_taxes", sa.Float(), nullable=True),
        sa.Column("state_sales_taxes", sa.Float(), nullable=True),
        sa.Column("total_annual_resources", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint(
            "family_type", "state", "place", "year", "analysis_type"
        ),
    )
    op.create_table(
        "city",
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("sss_city", sa.String(), nullable=False),
        sa.Column("census_name", sa.String(), nullable=True),
        sa.Column("population", sa.Integer(), nullable=True),
        sa.Column("public_transit", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("state", "place", "sss_city"),
    )
    op.create_table(
        "geo_identifier",
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("state_fips", sa.String(), nullable=True),
        sa.Column("county_fips", sa.String(), nullable=True),
        sa.Column("place_fips", sa.String(), nullable=True),
        sa.Column("cpi_region", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("state", "place"),
    )
    op.create_table(
        "health_care",
        sa.Column("family_type", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("analysis_type", sa.String(), nullable=False),
        sa.Column("premium", sa.Float(), nullable=True),
        sa.Column("out_of_pocket", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint(
            "family_type", "state", "place", "year", "analysis_type"
        ),
    )
    op.create_table(
        "miscellaneous",
        sa.Column("family_type", sa.String(), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("year", sa.String(), nullable=False),
        sa.Column("analysis_type", sa.String(), nullable=False),
        sa.Column("broadband_and_cell_phone", sa.Float(), nullable=True),
        sa.Column("other_necessities", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint(
            "family_type", "place", "state", "year", "analysis_type"
        ),
    )
    op.create_table(
        "puma",
        sa.Column("summary_level", sa.String(), nullable=True),
        sa.Column("state_fips", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("puma_code", sa.String(), nullable=False),
        sa.Column("county_fips", sa.String(), nullable=True),
        sa.Column("county_sub_fips", sa.String(), nullable=True),
        sa.Column("county_sub", sa.String(), nullable=True),
        sa.Column("county", sa.String(), nullable=True),
        sa.Column("puma_area", sa.String(), nullable=True),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("population", sa.Integer(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("state", "puma_code", "place"),
    )
    op.create_table(
        "report",
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("analysis_type", sa.String(), nullable=False),
        sa.Column("cpi_month", sa.String(), nullable=True),
        sa.Column("cpi_year", sa.Integer(), nullable=True),
        sa.Column("update_date", sa.Date(), nullable=True),
        sa.Column("update_person", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("year", "state", "analysis_type"),
    )
    op.create_table(
        "self_sufficiency_standard",
        sa.Column("family_type", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("analysis_type", sa.String(), nullable=False),
        sa.Column("adult", sa.Integer(), nullable=True),
        sa.Column("infant", sa.Integer(), nullable=True),
        sa.Column("preschooler", sa.Integer(), nullable=True),
        sa.Column("schoolager", sa.Integer(), nullable=True),
        sa.Column("teenager", sa.Integer(), nullable=True),
        sa.Column("weighted_child_count", sa.Integer(), nullable=True),
        sa.Column("housing", sa.Float(), nullable=True),
        sa.Column("child_care", sa.Float(), nullable=True),
        sa.Column("transportation", sa.Float(), nullable=True),
        sa.Column("health_care", sa.Float(), nullable=True),
        sa.Column("miscellaneous", sa.Float(), nullable=True),
        sa.Column("taxes", sa.Float(), nullable=True),
        sa.Column("earned_income_tax_credit", sa.Float(), nullable=True),
        sa.Column("child_care_tax_credit", sa.Float(), nullable=True),
        sa.Column("child_tax_credit", sa.Float(), nullable=True),
        sa.Column("hourly_self_sufficiency_wage", sa.Float(), nullable=True),
        sa.Column("monthly_self_sufficiency_wage", sa.Float(), nullable=True),
        sa.Column("annual_self_sufficiency_wage", sa.Float(), nullable=True),
        sa.Column("emergency_savings", sa.Float(), nullable=True),
        sa.Column("miscellaneous_is_secondary", sa.Boolean(), nullable=True),
        sa.Column("health_care_is_secondary", sa.Boolean(), nullable=True),
        sa.Column("analysis_is_secondary", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint(
            "family_type", "state", "place", "year", "analysis_type"
        ),
    )


def downgrade() -> None:
    op.drop_table("self_sufficiency_standard")
    op.drop_table("report")
    op.drop_table("puma")
    op.drop_table("miscellaneous")
    op.drop_table("health_care")
    op.drop_table("geo_identifier")
    op.drop_table("city")
    op.drop_table("arpa")
