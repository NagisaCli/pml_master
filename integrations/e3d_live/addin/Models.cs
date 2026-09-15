using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text;

namespace E3DLiveBridge.Addin
{
    internal static class BridgeConstants
    {
        internal const string ProtocolVersion = "2.0";
        internal const string AddinVersion = "0.3.0";
        internal const string Source = "e3d-caf-addin";
        internal const string ControlledWriteMode = "controlled_write";
    }

    [DataContract]
    internal sealed class ScopeDto
    {
        [DataMember(Name = "project_code", Order = 1)]
        public string ProjectCode { get; set; }

        [DataMember(Name = "mdb", Order = 2)]
        public string Mdb { get; set; }

        [DataMember(Name = "module", Order = 3)]
        public string Module { get; set; }

        public string DisplayName
        {
            get { return ProjectCode + "/" + Mdb + "/" + Module; }
        }
    }

    [DataContract]
    internal sealed class SessionFileDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "bridge_session_id", Order = 2)]
        public string BridgeSessionId { get; set; }

        [DataMember(Name = "token", Order = 3)]
        public string Token { get; set; }

        [DataMember(Name = "gateway_url", Order = 4)]
        public string GatewayUrl { get; set; }

        [DataMember(Name = "target_process_id", Order = 5)]
        public int TargetProcessId { get; set; }

        [DataMember(Name = "scope", Order = 6)]
        public ScopeDto Scope { get; set; }

        [DataMember(Name = "access_mode", Order = 7)]
        public string AccessMode { get; set; }

        [DataMember(Name = "write_enabled", Order = 8)]
        public bool WriteEnabled { get; set; }
    }

    [DataContract]
    internal sealed class SessionDto
    {
        [DataMember(Name = "bridge_session_id", Order = 1)]
        public string BridgeSessionId { get; set; }

        [DataMember(Name = "process_id", Order = 2)]
        public int ProcessId { get; set; }

        [DataMember(Name = "source", Order = 3)]
        public string Source { get; set; }

        [DataMember(Name = "addin_version", Order = 4)]
        public string AddinVersion { get; set; }

        [DataMember(Name = "scope", Order = 5)]
        public ScopeDto Scope { get; set; }
    }

    [DataContract]
    internal sealed class SelectionDto
    {
        [DataMember(Name = "full_name", Order = 1)]
        public string FullName { get; set; }

        [DataMember(Name = "element_type", Order = 2)]
        public string ElementType { get; set; }

        [DataMember(Name = "owner_full_name", Order = 3)]
        public string OwnerFullName { get; set; }

        [DataMember(Name = "attributes", Order = 4)]
        public Dictionary<string, string> Attributes { get; set; }
    }

    [DataContract]
    internal sealed class SelectionEnvelopeDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "message_type", Order = 2)]
        public string MessageType { get; set; }

        [DataMember(Name = "request_id", Order = 3)]
        public string RequestId { get; set; }

        [DataMember(Name = "timestamp_utc", Order = 4)]
        public string TimestampUtc { get; set; }

        [DataMember(Name = "session", Order = 5)]
        public SessionDto Session { get; set; }

        [DataMember(Name = "selection", Order = 6)]
        public SelectionDto Selection { get; set; }
    }

    [DataContract]
    internal sealed class ChangePreviewRequestDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "message_type", Order = 2)]
        public string MessageType { get; set; }

        [DataMember(Name = "request_id", Order = 3)]
        public string RequestId { get; set; }

        [DataMember(Name = "timestamp_utc", Order = 4)]
        public string TimestampUtc { get; set; }

        [DataMember(Name = "session", Order = 5)]
        public SessionDto Session { get; set; }

        [DataMember(Name = "selection", Order = 6)]
        public SelectionDto Selection { get; set; }

        [DataMember(Name = "instruction", Order = 7)]
        public string Instruction { get; set; }

        internal static ChangePreviewRequestDto Create(
            SelectionEnvelopeDto selection,
            string instruction)
        {
            return new ChangePreviewRequestDto
            {
                ProtocolVersion = BridgeConstants.ProtocolVersion,
                MessageType = "change_preview_request",
                RequestId = Guid.NewGuid().ToString("D"),
                TimestampUtc = DateTime.UtcNow.ToString("o"),
                Session = selection.Session,
                Selection = selection.Selection,
                Instruction = instruction
            };
        }
    }

    [DataContract]
    internal sealed class BackendDto
    {
        [DataMember(Name = "kind", Order = 1)]
        public string Kind { get; set; }

        [DataMember(Name = "model", Order = 2)]
        public string Model { get; set; }
    }

    [DataContract]
    internal sealed class PreviewOperationDto
    {
        [DataMember(Name = "operation_id", Order = 1)]
        public string OperationId { get; set; }

        [DataMember(Name = "operation_type", Order = 2)]
        public string OperationType { get; set; }

        [DataMember(Name = "target_element", Order = 3)]
        public string TargetElement { get; set; }

        [DataMember(Name = "attribute", Order = 4)]
        public string Attribute { get; set; }

        [DataMember(Name = "expected_current_value", Order = 5)]
        public string ExpectedCurrentValue { get; set; }

        [DataMember(Name = "proposed_value", Order = 6)]
        public string ProposedValue { get; set; }

        [DataMember(Name = "reason", Order = 7)]
        public string Reason { get; set; }
    }

    [DataContract]
    internal sealed class ChangeSetDto
    {
        [DataMember(Name = "schema_version", Order = 1)]
        public string SchemaVersion { get; set; }

        [DataMember(Name = "change_set_id", Order = 2)]
        public string ChangeSetId { get; set; }

        [DataMember(Name = "status", Order = 3)]
        public string Status { get; set; }

        [DataMember(Name = "executable", Order = 4)]
        public bool Executable { get; set; }

        [DataMember(Name = "requires_user_approval", Order = 5)]
        public bool RequiresUserApproval { get; set; }

        [DataMember(Name = "expires_at_utc", Order = 6)]
        public string ExpiresAtUtc { get; set; }

        [DataMember(Name = "scope", Order = 7)]
        public ScopeDto Scope { get; set; }

        [DataMember(Name = "target_element", Order = 8)]
        public string TargetElement { get; set; }

        [DataMember(Name = "operations", Order = 9)]
        public List<PreviewOperationDto> Operations { get; set; }
    }

    [DataContract]
    internal sealed class ChangePreviewResponseDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "request_id", Order = 2)]
        public string RequestId { get; set; }

        [DataMember(Name = "status", Order = 3)]
        public string Status { get; set; }

        [DataMember(Name = "mode", Order = 4)]
        public string Mode { get; set; }

        [DataMember(Name = "backend", Order = 5)]
        public BackendDto Backend { get; set; }

        [DataMember(Name = "change_set", Order = 6)]
        public ChangeSetDto ChangeSet { get; set; }
    }

    [DataContract]
    internal sealed class ConfigureAssistantRequestDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "message_type", Order = 2)]
        public string MessageType { get; set; }

        [DataMember(Name = "bridge_session_id", Order = 3)]
        public string BridgeSessionId { get; set; }

        [DataMember(Name = "process_id", Order = 4)]
        public int ProcessId { get; set; }

        [DataMember(Name = "scope", Order = 5)]
        public ScopeDto Scope { get; set; }

        [DataMember(Name = "provider", Order = 6)]
        public string Provider { get; set; }

        [DataMember(Name = "model", Order = 7)]
        public string Model { get; set; }

        [DataMember(Name = "api_key", Order = 8)]
        public string ApiKey { get; set; }
    }

    [DataContract]
    internal sealed class ApplyAuthorizationRequestDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "message_type", Order = 2)]
        public string MessageType { get; set; }

        [DataMember(Name = "request_id", Order = 3)]
        public string RequestId { get; set; }

        [DataMember(Name = "timestamp_utc", Order = 4)]
        public string TimestampUtc { get; set; }

        [DataMember(Name = "session", Order = 5)]
        public SessionDto Session { get; set; }

        [DataMember(Name = "change_set_id", Order = 6)]
        public string ChangeSetId { get; set; }

        [DataMember(Name = "target_element", Order = 7)]
        public string TargetElement { get; set; }

        [DataMember(Name = "operation_ids", Order = 8)]
        public List<string> OperationIds { get; set; }

        [DataMember(Name = "persist_requested", Order = 9)]
        public bool PersistRequested { get; set; }

        internal static ApplyAuthorizationRequestDto Create(
            SelectionEnvelopeDto envelope,
            ChangeSetDto changeSet,
            bool persistRequested)
        {
            List<string> operationIds = new List<string>();
            foreach (PreviewOperationDto operation in changeSet.Operations)
            {
                operationIds.Add(operation.OperationId);
            }
            return new ApplyAuthorizationRequestDto
            {
                ProtocolVersion = BridgeConstants.ProtocolVersion,
                MessageType = "apply_authorization_request",
                RequestId = Guid.NewGuid().ToString("D"),
                TimestampUtc = DateTime.UtcNow.ToString("o"),
                Session = envelope.Session,
                ChangeSetId = changeSet.ChangeSetId,
                TargetElement = changeSet.TargetElement,
                OperationIds = operationIds,
                PersistRequested = persistRequested
            };
        }
    }

    [DataContract]
    internal sealed class ApplyAuthorizationResponseDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "request_id", Order = 2)]
        public string RequestId { get; set; }

        [DataMember(Name = "status", Order = 3)]
        public string Status { get; set; }

        [DataMember(Name = "authorization_id", Order = 4)]
        public string AuthorizationId { get; set; }

        [DataMember(Name = "change_set_id", Order = 5)]
        public string ChangeSetId { get; set; }

        [DataMember(Name = "expires_at_utc", Order = 6)]
        public string ExpiresAtUtc { get; set; }

        [DataMember(Name = "scope", Order = 7)]
        public ScopeDto Scope { get; set; }

        [DataMember(Name = "target_element", Order = 8)]
        public string TargetElement { get; set; }

        [DataMember(Name = "persist_requested", Order = 9)]
        public bool PersistRequested { get; set; }

        [DataMember(Name = "operations", Order = 10)]
        public List<PreviewOperationDto> Operations { get; set; }
    }

    [DataContract]
    internal sealed class ApplyOperationResultDto
    {
        [DataMember(Name = "operation_id", Order = 1)]
        public string OperationId { get; set; }

        [DataMember(Name = "attribute", Order = 2)]
        public string Attribute { get; set; }

        [DataMember(Name = "before_value", Order = 3)]
        public string BeforeValue { get; set; }

        [DataMember(Name = "requested_value", Order = 4)]
        public string RequestedValue { get; set; }

        [DataMember(Name = "after_value", Order = 5)]
        public string AfterValue { get; set; }

        [DataMember(Name = "status", Order = 6)]
        public string Status { get; set; }
    }

    [DataContract]
    internal sealed class ApplyResultRequestDto
    {
        [DataMember(Name = "protocol_version", Order = 1)]
        public string ProtocolVersion { get; set; }

        [DataMember(Name = "message_type", Order = 2)]
        public string MessageType { get; set; }

        [DataMember(Name = "request_id", Order = 3)]
        public string RequestId { get; set; }

        [DataMember(Name = "timestamp_utc", Order = 4)]
        public string TimestampUtc { get; set; }

        [DataMember(Name = "session", Order = 5)]
        public SessionDto Session { get; set; }

        [DataMember(Name = "authorization_id", Order = 6)]
        public string AuthorizationId { get; set; }

        [DataMember(Name = "change_set_id", Order = 7)]
        public string ChangeSetId { get; set; }

        [DataMember(Name = "target_element", Order = 8)]
        public string TargetElement { get; set; }

        [DataMember(Name = "status", Order = 9)]
        public string Status { get; set; }

        [DataMember(Name = "persistence", Order = 10)]
        public string Persistence { get; set; }

        [DataMember(Name = "message", Order = 11)]
        public string Message { get; set; }

        [DataMember(Name = "operation_results", Order = 12)]
        public List<ApplyOperationResultDto> OperationResults { get; set; }
    }

    internal static class JsonCodec
    {
        private static DataContractJsonSerializer CreateSerializer(Type type)
        {
            return new DataContractJsonSerializer(
                type,
                new DataContractJsonSerializerSettings
                {
                    UseSimpleDictionaryFormat = true
                });
        }

        internal static string Serialize<T>(T value)
        {
            using (MemoryStream stream = new MemoryStream())
            {
                CreateSerializer(typeof(T)).WriteObject(stream, value);
                return Encoding.UTF8.GetString(stream.ToArray());
            }
        }

        internal static T Deserialize<T>(string json)
        {
            byte[] bytes = Encoding.UTF8.GetBytes(json);
            using (MemoryStream stream = new MemoryStream(bytes))
            {
                return (T)CreateSerializer(typeof(T)).ReadObject(stream);
            }
        }
    }
}
