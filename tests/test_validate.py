import pytest

from back.schemas import valid_wallet_address, parse_cf_v1_address


@pytest.mark.parametrize(
    "net_name, address, result", [
        ("raiden",      "jrmnGqeeds4Dp67AZkYH4ox6XHMtJLdG8n4V1HBcBT8S2x21DE5LGrbYXMZTsXPsuY8NpXxSoE2wSYTn5TmGTd1y7ftL4MzqdtvHVaub", True),
        ("backbone",    "jrmnGqeeds4Dp67AZkYH4ox6XHMtJLdG8n4V1HBcBT8S2x21DE5LGrbYXMZTsXPsuY8NpXxSoE2wSYTn5TmGTd1y7ftL4MzqdtvHVaub", False),
        ("raiden",      "jrmnGqeeds4Dp67AbEdAzqyCrPZnZd5abbfvjWowyjzMh2NoteqBxrJCzZGRVZDxqUt9wyh4wfcNE8hoNdmfZ2jYWSm1KbgXrZ11woSj", True),
        ("backbone",    "jrmnGqeeds4Dp67AbEdAzqyCrPZnZd5abbfvjWowyjzMh2NoteqBxrJCzZGRVZDxqUt9wyh4wfcNE8hoNdmfZ2jYWSm1KbgXrZ11woSj", False),
        ("raiden",      "jrmnGqeeds4bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", False),
        ("raiden",      "xrmnGqeeds4bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", False),
        ("raiden",      "helloworld", False),
        ("raiden",      "jrmnGqeeds!!!!!!!!!!!!", False),
        ("unknown net",      "", False),
        ("unknown net",      "1", False),
        ("unknown net",      "!", False),
        ("unknown net",      "[]", False),
    ]
)
def test_valid_address(net_name, address, result):
    assert valid_wallet_address(net_name, address) == result


