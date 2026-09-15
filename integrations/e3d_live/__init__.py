"""Isolated live bridge between AVEVA E3D and an AI gateway."""

from .protocol import PROTOCOL_VERSION, ProtocolError, ScopeKey

__all__ = ["PROTOCOL_VERSION", "ProtocolError", "ScopeKey"]
