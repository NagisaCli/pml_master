using System;
using System.Diagnostics;
using System.IO;

namespace E3DLiveBridge.Addin
{
    internal sealed class BridgeConfiguration
    {
        internal string BridgeSessionId { get; private set; }
        internal string Token { get; private set; }
        internal Uri GatewayBaseUri { get; private set; }
        internal ScopeDto ExpectedScope { get; private set; }
        internal int TargetProcessId { get; private set; }
        internal string AccessMode { get; private set; }
        internal bool WriteEnabled { get; private set; }

        internal static string SessionFilePath
        {
            get
            {
                string root = Environment.GetEnvironmentVariable("E3D_LIVE_SESSION_ROOT");
                if (String.IsNullOrWhiteSpace(root))
                {
                    string local = Environment.GetFolderPath(
                        Environment.SpecialFolder.LocalApplicationData);
                    root = Path.Combine(local, "E3DLiveBridge", "sessions");
                }

                return Path.Combine(
                    Path.GetFullPath(root),
                    Process.GetCurrentProcess().Id.ToString() + ".json");
            }
        }

        internal static bool TryLoad(out BridgeConfiguration configuration, out string error)
        {
            configuration = null;
            error = String.Empty;
            try
            {
                string path = SessionFilePath;
                if (!File.Exists(path))
                {
                    error = "Gateway session file not found: " + path;
                    return false;
                }

                SessionFileDto data = JsonCodec.Deserialize<SessionFileDto>(
                    File.ReadAllText(path));
                if (data == null || data.ProtocolVersion != BridgeConstants.ProtocolVersion)
                {
                    error = "Gateway protocol version is missing or incompatible.";
                    return false;
                }
                if (!String.Equals(data.AccessMode, "read_only", StringComparison.Ordinal) &&
                    !String.Equals(
                        data.AccessMode,
                        BridgeConstants.ControlledWriteMode,
                        StringComparison.Ordinal))
                {
                    error = "Gateway access mode is missing or unsupported.";
                    return false;
                }
                bool expectedWriteEnabled = String.Equals(
                    data.AccessMode,
                    BridgeConstants.ControlledWriteMode,
                    StringComparison.Ordinal);
                if (data.WriteEnabled != expectedWriteEnabled)
                {
                    error = "Gateway access-mode flags are inconsistent.";
                    return false;
                }
                int currentProcessId = Process.GetCurrentProcess().Id;
                if (data.TargetProcessId != currentProcessId)
                {
                    error = "Gateway targets E3D PID " + data.TargetProcessId +
                        ", but this E3D process is PID " + currentProcessId + ".";
                    return false;
                }
                if (data.Scope == null)
                {
                    error = "Gateway scope is missing.";
                    return false;
                }
                if (String.IsNullOrWhiteSpace(data.BridgeSessionId) ||
                    String.IsNullOrWhiteSpace(data.Token) ||
                    String.IsNullOrWhiteSpace(data.GatewayUrl))
                {
                    error = "Gateway session id, token, or URL is missing.";
                    return false;
                }

                Uri gatewayUri;
                if (!Uri.TryCreate(data.GatewayUrl, UriKind.Absolute, out gatewayUri) ||
                    gatewayUri.Scheme != Uri.UriSchemeHttp ||
                    !gatewayUri.IsLoopback ||
                    !String.Equals(gatewayUri.Host, "127.0.0.1", StringComparison.Ordinal) ||
                    gatewayUri.Port <= 0 || gatewayUri.Port > 65535 ||
                    !String.Equals(gatewayUri.AbsolutePath, "/", StringComparison.Ordinal) ||
                    !String.IsNullOrEmpty(gatewayUri.UserInfo) ||
                    !String.IsNullOrEmpty(gatewayUri.Query) ||
                    !String.IsNullOrEmpty(gatewayUri.Fragment))
                {
                    error = "Gateway URL must be an exact 127.0.0.1 HTTP origin.";
                    return false;
                }

                data.Scope.ProjectCode = Normalise(data.Scope.ProjectCode);
                data.Scope.Mdb = Normalise(data.Scope.Mdb);
                data.Scope.Module = Normalise(data.Scope.Module);
                if (String.IsNullOrEmpty(data.Scope.ProjectCode) ||
                    String.IsNullOrEmpty(data.Scope.Mdb) ||
                    String.IsNullOrEmpty(data.Scope.Module))
                {
                    error = "Gateway scope contains an empty value.";
                    return false;
                }

                configuration = new BridgeConfiguration
                {
                    BridgeSessionId = data.BridgeSessionId,
                    Token = data.Token,
                    GatewayBaseUri = gatewayUri,
                    ExpectedScope = data.Scope,
                    TargetProcessId = data.TargetProcessId,
                    AccessMode = data.AccessMode,
                    WriteEnabled = data.WriteEnabled
                };
                return true;
            }
            catch (Exception exception)
            {
                error = "Unable to read gateway session: " + exception.Message;
                return false;
            }
        }

        internal static string Normalise(string value)
        {
            return (value ?? String.Empty).Trim().TrimStart('/').ToUpperInvariant();
        }
    }
}
