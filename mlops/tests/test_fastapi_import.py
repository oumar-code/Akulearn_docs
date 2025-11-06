def test_import_fastapi_app():
    # Ensure the FastAPI app file parses and can be imported
    import importlib
    spec = importlib.util.spec_from_file_location("fastapi_app", "mlops/examples/fastapi_server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "app")
