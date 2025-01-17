from cdapython import Q
import pytest


def test_sql_wrong_table():
    with pytest.raises(Exception) as excinfo:
        Q.sql(
            """
        select acc, biosample, bioproject, releasedate, librarylayout, mbases, organism
        FROM nih-sra-datastore.sra.metadata
        WHERE platform = "ILLUMINA" AND librarysource = "METAGENOMIC" AND consent = "public" AND assay_type = "WGS" AND libraryselection = "RANDOM"
        """
        )
    assert str(excinfo.value) == "Your database is outside of the project"
