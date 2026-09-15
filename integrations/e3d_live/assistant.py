"""Read-only assistant backend for the first live-bridge milestone."""

from __future__ import annotations

from .preview import ChangePreview, ChangePreviewRequest, local_preview
from .protocol import GatewayResponse, SelectionEnvelope


class ReadOnlyAssistant:
    """A deterministic backend that proves transport without model mutation.

    This intentionally does not import a language-model client or repository
    knowledge.  A later backend must receive an explicit, scope-approved context
    bundle rather than consulting global memory.
    """

    backend_name = "local_only"
    model_name = None

    def analyse(self, envelope: SelectionEnvelope) -> GatewayResponse:
        selected = envelope.selection
        message = (
            f"Read-only snapshot accepted for {selected.element_type} "
            f"{selected.full_name}. {len(selected.attributes)} allowlisted "
            "attributes were received. No E3D changes were generated."
        )
        return GatewayResponse(
            request_id=envelope.request_id,
            status="read_only",
            message=message,
            scope=envelope.scope,
        )

    def preview(self, request: ChangePreviewRequest) -> ChangePreview:
        return local_preview(request)
