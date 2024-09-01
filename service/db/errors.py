class UnexpectedDBError(Exception):
    """
    Exception throws when facing an unexpected error during a DB operation
    """
    pass


class MissingRecordDBError(Exception):
    """
    Exception thrown when trying to operate (delete/update/etc) on a non-existent record.
    """
    pass


class RecordAlreadyExists(Exception):
    """
    Exception thrown when trying to create a record which already exists (by primary key).
    """
    pass
