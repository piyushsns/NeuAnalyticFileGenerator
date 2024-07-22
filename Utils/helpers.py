# utils/helpers.py

queries = {
    "TM01": """SELECT
            LEFT(COALESCE(debt.external_account_id2, '') + SPACE(30), 30) +              -- Account Number (30 characters)
            LEFT(COALESCE('16256059', '') + SPACE(30), 30) +       -- Vendor Account Number (30 characters)
            LEFT(COALESCE('Syncom', '') + SPACE(10), 10) +                 -- Vendor Code (10 characters)
            LEFT(COALESCE('DEF1', '') + SPACE(10), 10) +              -- Portfolio Code (10 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, FORMAT(entry.settled_on, 'yyyyMMdd'), 120), '') + SPACE(8), 8) +  -- Transaction Date (8 characters)
            LEFT(COALESCE('', '') + SPACE(6), 6) +             -- Transaction Time (6 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '1'), '') + SPACE(3), 3) + -- Transaction Sequence (3 characters)
            -- LEFT(COALESCE(CONVERT(VARCHAR, ROW_NUMBER() OVER (ORDER BY (SELECT NULL))), '') + SPACE(3), 3) + -- Transaction Sequence (3 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, entry.amount), '') + SPACE(13), 13) +   -- Transaction Amount (13 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, debt.initial_balance), '') + SPACE(13), 13) +  -- Transaction Principal Amount (13 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '0.0'), '0.0') + SPACE(13), 13) + -- Transaction Interest Amount (13 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '0.0'), '0.0') + SPACE(13), 13) + -- Transaction Late Fees Amount (13 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '0.0'), '0.0') + SPACE(13), 13) + -- Transaction Court Costs Amount (13 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '0.0'), '0.0') + SPACE(13), 13) + -- Transaction Other Fees Amount (13 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, entry.entry_type_id), '') + SPACE(1), 2) +   -- Transaction Type (2 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '1'), '') + SPACE(1), 2) +     -- Payment Method (2 characters)
            LEFT(COALESCE('1', '') + SPACE(25), 25) +                -- Collector ID (25 characters)
            LEFT(COALESCE('1', '') + SPACE(4), 4) +       -- Client Transaction Code (4 characters)
            LEFT(COALESCE(CONVERT(VARCHAR, '1'), '') + SPACE(3), 3)    -- Plan ID (3 characters)
            AS combined_column
        FROM
            debt
        JOIN
            entry ON entry.account_id = debt.account_id
        JOIN
            entry_type ON entry_type.id = entry.entry_type_id""",
    "TPF0": """SELECT
                LEFT(COALESCE(debt.external_account_id2, '') + SPACE(30), 30) +  -- Account Number (30 characters)
                LEFT(COALESCE('16256059', '16256059') + SPACE(30), 30) +  -- Vendor Account Number (30 characters, assuming empty)
                LEFT(COALESCE('Syncom', 'Syncom') + SPACE(10), 10) +  -- Vendor Code (10 characters, assuming empty)
                LEFT(COALESCE('DEF1', 'DEF1') + SPACE(10), 10) +  -- Portfolio Code (10 characters, assuming empty)
                LEFT(COALESCE(CONVERT(VARCHAR, '', 112), '') + SPACE(8), 8) +  -- Plan Payment Expected Date (8 characters)
                RIGHT(SPACE(3) + COALESCE(CONVERT(VARCHAR, ROW_NUMBER() OVER (ORDER BY (SELECT NULL))), ''), 3) +  -- Plan Payment Sequence (3 characters)
                RIGHT(SPACE(13) + COALESCE(CONVERT(VARCHAR, ''), ''), 13) +  -- Plan Payment Amount (13 characters)
                RIGHT(SPACE(3) + COALESCE(CONVERT(VARCHAR, ''), ''), 3)  -- Plan ID (3 characters)
                AS combined_column
            FROM
                debt
            JOIN
                entry ON entry.account_id = debt.account_id
            JOIN
                entry_type ON entry_type.id = entry.entry_type_id""",  # Replace with actual query
}


def getQueryByRecordType(record_type):
    return queries.get(record_type, "")
