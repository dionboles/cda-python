from json import loads
from logging import error as logError
import logging
from multiprocessing.pool import ApplyResult
from typing import Optional
from urllib3.exceptions import InsecureRequestWarning, SSLError
from cdapython.Result import Result, get_query_result
from cdapython.functions import col, quoted, unquoted
from cda_client.api.meta_api import MetaApi
from cdapython.decorators import measure
from typing import Union
import cdapython.constantVariables as const
from cda_client.exceptions import ServiceException
from cdapython.functions import find_ssl_path
from urllib3.connection import NewConnectionError
from urllib3.connectionpool import MaxRetryError
from cdapython.errorLogger import deprecated_values, unverfiedHttp
from cda_client.model.query import Query
from cda_client.api.query_api import QueryApi
from cda_client import ApiClient, Configuration
from cda_client.model.query_created_data import QueryCreatedData
from cdapython.constantVariables import table_version, default_table, project_name
from cdapython.ConvertionMap import convertionMap
logging.captureWarnings(InsecureRequestWarning)


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    def __init__(self, *args: Union[str, Query]) -> None:
        """

        Args:
            *args (object):
        """
        self.query = Query()

        if len(args) == 1:

            if args[0] is None:
                raise RuntimeError("Q statement parse error")

            _l, _op, _r = args[0].split(" ", 2)
            
            if _l in convertionMap:
                tmpL = convertionMap[_l]
                deprecated_values(old=_l,new=tmpL)
                _l = tmpL

            _l = col(_l)
            _r = infer_quote(_r)
        elif len(args) != 3:
            raise RuntimeError(
                "Require one or three arguments. Please see documentation."
            )
        else:
            _l = infer_quote(args[0])
            _op = args[1]
            _r = infer_quote(args[2])

        self.query.node_type = _op
        self.query.l = _l
        self.query.r = _r

    def __repr__(self) -> str:
        return str(self.__class__) + ": \n" + str(self.__dict__)

    @staticmethod
    def set_host_url(url: str) -> None:
        const.CDA_API_URL = url

    @staticmethod
    def get_host_url() -> Optional[str]:
        return const.CDA_API_URL

    @staticmethod
    def sql(
        sql: str,
        host: Optional[str] = None,
        dry_run: bool = False,
        offset: int = 0,
        limit: int = 100,
        verify: Optional[bool] = None,
    ) -> Optional[Result]:
        """[summary]

        Args:
            sql (str): [description]
            host (Optional[str], optional): [description]. Defaults to None.
            dry_run (bool, optional): [description]. Defaults to False.
            offset (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.
            verify (Optional[bool], optional): [description].
            Defaults to None.

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """

        tmp_configuration: Configuration = Configuration(host=host)
        if (
            "create table" in sql.lower()
            or "delete from" in sql.lower()
            or "drop table" in sql.lower()
        ):
            raise Exception("Those actions are not available in Q.sql")

        if project_name is not None and sql.find(project_name) == -1:
            raise Exception("Your database is outside of the project")

        if host is None:
            host = const.CDA_API_URL

        if verify is None:
            tmp_configuration.verify_ssl = find_ssl_path()

        if verify is False:
            unverfiedHttp()
            tmp_configuration.verify_ssl = False
        cda_client_obj = ApiClient(configuration=tmp_configuration)
        try:

            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.sql_query(sql)
            if dry_run is True:
                return api_response
            return get_query_result(api_instance, api_response.query_id, offset, limit)

        except Exception as e:
            print(e)
        return None

    @staticmethod
    def statusbigquery() -> str:
        """[summary]
        Uses the cda_client library's MetaClass to get status check on the cda
        BigQuery table
        Returns:
            str: status messages
        """
        return MetaApi().service_status()["systems"]["BigQueryStatus"]["messages"][0]

    @staticmethod
    def queryjobstatus(
        id: str, host: Optional[str] = None, verify: Optional[bool] = None
    ):
        """[summary]

        Args:
            id (str): [description]
            host (Optional[str], optional): [description].
            Defaults to None.
            verify (Optional[bool], optional):
            [description]. Defaults to None.

        Returns:
            object: [description]
        """
        tmp_configuration: Configuration = Configuration(host=host)

        if host is None:
            host = const.CDA_API_URL

        if verify is None:
            tmp_configuration.verify_ssl = find_ssl_path()

        if verify is False:
            unverfiedHttp()
            tmp_configuration.verify_ssl = False
        cda_client_obj = ApiClient(configuration=tmp_configuration)
        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.job_status(id)
                print(type(api_response))
                return api_response["status"]

        except InsecureRequestWarning as e:
            print(e)
        except Exception as e:
            print(e)

    @measure
    def run(
        self,
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = table_version,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = default_table,
        async_call: bool = False,
        verify: Optional[bool] = None,
    ) -> Union[QueryCreatedData, ApplyResult, Result, None]:

        """[summary]

        Args:
            offset (int, optional): [description].
            Defaults to 0.
            limit (int, optional): [description].
            Defaults to 100.
            version (Optional[str], optional): [description].
            Defaults to table_version.
            host (Optional[str], optional): [description].
            Defaults to None.
            dry_run (bool, optional): [description].
            'Defaults to False.
            table (Optional[str], optional): [description].
            Defaults to default_table.
            async_call (bool, optional): [description].
            Defaults to False.
            verify (Optional[bool], optional): [description].
            Defaults to None.

        Returns:
            Union[
                QueryCreatedData,
                ApplyResult,
                Result,
                None
            ]: [description]
        """
        tmp_configuration: Configuration = Configuration(host=host)
        if host is None:
            host = const.CDA_API_URL
        if verify is None:
            tmp_configuration.verify_ssl = find_ssl_path()
        if verify is False:
            unverfiedHttp()
            tmp_configuration.verify_ssl = False
        cda_client_obj = ApiClient(configuration=tmp_configuration)

        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                # Execute boolean query
                print("Getting results from database", end="\n\n")
                api_response: Union[
                    QueryCreatedData, ApplyResult
                ] = api_instance.boolean_query(
                    self.query,
                    version=version,
                    dry_run=dry_run,
                    table=table,
                    async_req=async_call,
                )

                if isinstance(api_response, ApplyResult):
                    print("Waiting for results")
                    while api_response.ready() is False:
                        api_response.wait(10000)
                    api_response = api_response.get()

                if dry_run is True:
                    return api_response

                return get_query_result(
                    api_instance, api_response.query_id, offset, limit
                )
        except ServiceException as httpError:
            if httpError.body is not None:
                logError(
                    f"""
                Http Status: {httpError.status}
                Error Message: {loads(httpError.body)["message"]}
                """
                )

        except NewConnectionError as e:
            print("Connection error")

        except SSLError as e:
            print(e)

        except InsecureRequestWarning as e:
            print(
                "Adding certificate verification pem is strongly advised please read our https://cda.readthedocs.io/en/latest/Installation.html "
            )

        except MaxRetryError as e:
            print(
                f"Connection error max retry limit of 3 hit please check url or local python ssl pem {e}"
            )

        except Exception as e:
            print(e)
        return None

    def And(self, right: "Q") -> "Q":
        return Q(self.query, "AND", right.query)

    def Or(self, right: "Q") -> "Q":
        return Q(self.query, "OR", right.query)

    def From(self, right: "Q") -> "Q":
        return Q(self.query, "SUBQUERY", right.query)

    def Not(self) -> "Q":
        return Q(self.query, "NOT", None)

    def Not_EQ(self, right: "Q") -> "Q":
        return Q(self.query, "!=", right.query)

    def Greater_Then_EQ(self, right: "Q"):
        return Q(self.query, ">=", right.query)

    def Greater_Then(self, right: "Q"):
        return Q(self.query, ">", right.query)

    def Less_Then_EQ(self, right: "Q"):
        return Q(self.query, "<=", right.query)

    def Less_Then(self, right: "Q"):
        return Q(self.query, "<", right.query)


def infer_quote(val: Union[str, "Q", Query]) -> Union[Q, Query]:
    """[summary]
    Handles Strings With quotes
    Args:
        val (Union[str,"Q",Query): [description]

    Returns:
        Query: [description]
    """
    if isinstance(val, (Q, Query)):
        return val
    if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return quoted(val[1:-1])
    return unquoted(val)
