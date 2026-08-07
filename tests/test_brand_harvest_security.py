from __future__ import annotations

import importlib.util
import socket
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "Skills/brand-harvester/scripts/brand_harvest.py"
SPEC = importlib.util.spec_from_file_location("brand_harvest", MODULE_PATH)
assert SPEC and SPEC.loader
brand_harvest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(brand_harvest)


class BrandSourceUrlSecurityTests(unittest.TestCase):
    def test_rejects_non_http_schemes(self) -> None:
        for url in ("file:///etc/passwd", "ftp://example.com/file", "data:text/plain,hello"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                brand_harvest.ensure_url(url)

    def test_rejects_local_and_private_literals(self) -> None:
        blocked = (
            "http://localhost/",
            "http://127.0.0.1/",
            "http://[::1]/",
            "http://169.254.169.254/latest/meta-data/",
            "http://10.0.0.1/",
            "http://172.16.0.1/",
            "http://192.168.1.1/",
            "http://[fc00::1]/",
            "http://[fe80::1]/",
        )
        for url in blocked:
            with self.subTest(url=url), self.assertRaises(ValueError):
                brand_harvest.ensure_url(url)

    @mock.patch.object(socket, "getaddrinfo")
    def test_rejects_hostname_resolving_to_private_address(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.20.30.40", 443))
        ]
        with self.assertRaises(ValueError):
            brand_harvest.validate_public_url("https://brand.example/", resolve_dns=True)

    @mock.patch.object(socket, "getaddrinfo")
    def test_accepts_public_http_and_https(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        ]
        self.assertEqual(
            brand_harvest.validate_public_url("https://example.com/brand", resolve_dns=True),
            "https://example.com/brand",
        )
        self.assertEqual(brand_harvest.ensure_url("example.com"), "https://example.com")

    @mock.patch.object(socket, "getaddrinfo")
    def test_redirect_handler_rejects_private_target(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 80))
        ]
        handler = brand_harvest.SafeRedirectHandler()
        request = brand_harvest.urllib.request.Request("https://example.com/")
        with self.assertRaises(ValueError):
            handler.redirect_request(
                request,
                None,
                302,
                "Found",
                {},
                "http://redirect.example/private",
            )

    def test_redirect_handler_rejects_metadata_literal_before_follow(self) -> None:
        handler = brand_harvest.SafeRedirectHandler()
        request = brand_harvest.urllib.request.Request("https://example.com/")
        with self.assertRaises(ValueError):
            handler.redirect_request(
                request,
                None,
                302,
                "Found",
                {},
                "http://169.254.169.254/latest/meta-data/",
            )

    @mock.patch.object(socket, "getaddrinfo")
    def test_authenticated_redirect_cannot_change_host(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        ]
        handler = brand_harvest.SafeRedirectHandler({"api.brandfetch.io"})
        request = brand_harvest.urllib.request.Request(
            "https://api.brandfetch.io/v2/brands/domain/example.com",
            headers={"Authorization": "Bearer test-only"},
        )
        with self.assertRaises(ValueError):
            handler.redirect_request(
                request,
                None,
                302,
                "Found",
                {},
                "https://redirect.example/capture",
            )


if __name__ == "__main__":
    unittest.main()
