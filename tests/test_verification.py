from tools.verify_entries import verify_entry


def test_generic_rpc_probes_never_verify_named_errors():
    entry = {"id": "require-auth-missing", "category": "host-error", "error_code": "HostError::AuthMissing", "verified": True}
    for response in [
        {"result": {"error": "Could not unmarshal transaction"}},
        {"result": {"passphrase": "Test SDF Network ; September 2015"}},
        {"error": {"message": "offline"}},
        {"result": {"error": "HostError::AuthMissing"}},
    ]:
        report = verify_entry(entry, "https://example.com", 123, response)
        assert report["verified"] is False
        assert report["status"] == "REVIEW_REQUIRED"
        assert report["details"]["response"] == response
