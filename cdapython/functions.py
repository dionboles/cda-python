from typing import Optional, Union
from cda_client.model.query import Query
from os import path
from ssl import get_default_verify_paths


def col(col_name: Optional[str]) -> Query:
    return Query(node_type="column", value=col_name)


def quoted(quoted_val: Optional[str]) -> Query:
    return Query(node_type="quoted", value=quoted_val)


def unquoted(val: Optional[Union[str, Query]]) -> Query:
    return Query(node_type="unquoted", value=val)


def find_ssl_path() -> bool:
    """[summary]
    This will look in your local computer for a ssl pem file and
    return True or False if the file is there.
    if value is False Q will accept any TLS certificate presented by a server,
    and will ignore hostname mismatches and expired certificates
    Returns:
        bool: [description]
    """
    openssl_dir, openssl_cafile = path.split(get_default_verify_paths().openssl_cafile)
    check: bool = True

    if not path.exists(openssl_dir):
        check = False

    if openssl_cafile.find("pem") == -1:
        check = False

    return check
