using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Aveva.ApplicationFramework;
using Aveva.ApplicationFramework.Presentation;
using Aveva.Core.Database;

namespace E3DLiveBridge.Addin
{
    public sealed class E3DLiveBridgeAddin : IAddinInjected
    {
        private DockedWindow window;
        private E3DLiveBridgeControl control;
        private SelectionEnvelopeDto currentEnvelope;
        private BridgeConfiguration currentConfiguration;
        private ChangeSetDto pendingChangeSet;
        private int requestSequence;
        private bool isApplying;

        public string Name { get { return "E3DLiveBridge.Addin"; } }

        public string Description
        {
            get { return "PID-scoped AI preview and operator-confirmed E3D changes."; }
        }

        public void Start(IDependencyResolver resolver) { Initialise(); }

        public void Start(ServiceManager serviceManager)
        {
            // Retained for the inherited IAddin contract used by E3D 3.1.
        }

        public void Stop()
        {
            CurrentElement.CurrentElementChanged -= CurrentElementChanged;
            if (control != null)
            {
                control.HealthRequested -= HealthRequested;
                control.SendRequested -= SendRequested;
                control.PreviewRequested -= PreviewRequested;
                control.ConfigureRequested -= ConfigureRequested;
                control.ApplyRequested -= ApplyRequested;
                control.Dispose();
                control = null;
            }
            currentEnvelope = null;
            currentConfiguration = null;
            pendingChangeSet = null;
        }

        private void Initialise()
        {
            IWindowManager windowManager =
                DependencyResolver.GetImplementationOf<IWindowManager>();
            control = new E3DLiveBridgeControl();
            window = windowManager.CreateDockedWindow(
                "E3DLiveBridge.Panel",
                "E3D AI Assistant (Controlled)",
                control,
                DockedPosition.Right);
            window.Width = 460;
            window.SaveLayout = true;

            ICommandManager commandManager =
                DependencyResolver.GetImplementationOf<ICommandManager>();
            commandManager.Commands.Add(new ShowBridgeCommand(window));

            control.HealthRequested += HealthRequested;
            control.SendRequested += SendRequested;
            control.PreviewRequested += PreviewRequested;
            control.ConfigureRequested += ConfigureRequested;
            control.ApplyRequested += ApplyRequested;
            CurrentElement.CurrentElementChanged += CurrentElementChanged;
            CaptureCurrentSelection(true);
        }

        private void CurrentElementChanged(object sender, CurrentElementChangedEventArgs args)
        {
            if (!isApplying)
            {
                CaptureCurrentSelection(true);
            }
        }

        private void CaptureCurrentSelection(bool invalidatePendingChangeSet)
        {
            if (invalidatePendingChangeSet)
            {
                pendingChangeSet = null;
                control.SetPendingChangeSet(false);
            }

            string error;
            BridgeConfiguration configuration;
            if (!BridgeConfiguration.TryLoad(out configuration, out error))
            {
                currentConfiguration = null;
                currentEnvelope = null;
                control.SetStatus(error, true);
                return;
            }

            SelectionEnvelopeDto envelope;
            if (!SelectionSnapshotBuilder.TryBuild(configuration, out envelope, out error))
            {
                currentConfiguration = configuration;
                currentEnvelope = null;
                control.SetScope(configuration.ExpectedScope.DisplayName);
                control.SetStatus(error, true);
                return;
            }

            currentConfiguration = configuration;
            currentEnvelope = envelope;
            control.SetScope(configuration.ExpectedScope.DisplayName);
            control.SetStatus(
                configuration.WriteEnabled
                    ? "selection captured; writes require preview and confirmation"
                    : "selection captured; gateway is read-only",
                false);
            control.SetSelection(envelope);
        }

        private void HealthRequested(object sender, EventArgs args)
        {
            string error;
            BridgeConfiguration configuration;
            if (!BridgeConfiguration.TryLoad(out configuration, out error))
            {
                control.SetStatus(error, true);
                return;
            }
            RunGatewayCall(
                configuration,
                delegate(GatewayClient client) { return client.GetHealth(); },
                delegate(string response)
                {
                    control.SetResponse(response);
                    CaptureCurrentSelection(true);
                },
                false);
        }

        private void SendRequested(object sender, EventArgs args)
        {
            if (!EnsureCurrentSelection()) { return; }
            BridgeConfiguration configuration = currentConfiguration;
            SelectionEnvelopeDto envelope = currentEnvelope;
            RunGatewayCall(
                configuration,
                delegate(GatewayClient client) { return client.PostSelection(envelope); },
                null,
                true);
        }

        private void ConfigureRequested(object sender, EventArgs args)
        {
            if (!EnsureCurrentSelection()) { return; }
            string apiKey = control.TakeApiKey();
            if (String.IsNullOrWhiteSpace(apiKey))
            {
                control.SetStatus("enter the selected provider API key before connecting", true);
                return;
            }
            ConfigureAssistantRequestDto request = new ConfigureAssistantRequestDto
            {
                ProtocolVersion = BridgeConstants.ProtocolVersion,
                MessageType = "configure_assistant",
                BridgeSessionId = currentConfiguration.BridgeSessionId,
                ProcessId = currentConfiguration.TargetProcessId,
                Scope = currentConfiguration.ExpectedScope,
                Provider = control.GetAssistantProvider(),
                Model = control.GetAssistantModel(),
                ApiKey = apiKey
            };
            BridgeConfiguration configuration = currentConfiguration;
            RunGatewayCall(
                configuration,
                delegate(GatewayClient client) { return client.PostConfigureAssistant(request); },
                delegate(string response)
                {
                    control.SetResponse(response);
                    control.SetStatus(
                        "AI provider configured; the first Preview validates connectivity",
                        false);
                },
                false);
        }

        private void PreviewRequested(object sender, EventArgs args)
        {
            string instruction = control.GetInstruction();
            if (String.IsNullOrWhiteSpace(instruction))
            {
                control.SetStatus("enter a change instruction before previewing", true);
                return;
            }
            if (!EnsureCurrentSelection()) { return; }

            pendingChangeSet = null;
            control.SetPendingChangeSet(false);
            BridgeConfiguration configuration = currentConfiguration;
            SelectionEnvelopeDto envelope = currentEnvelope;
            ChangePreviewRequestDto preview = ChangePreviewRequestDto.Create(envelope, instruction);
            RunGatewayCall(
                configuration,
                delegate(GatewayClient client) { return client.PostPreview(preview); },
                delegate(string response)
                {
                    ChangePreviewResponseDto parsed =
                        JsonCodec.Deserialize<ChangePreviewResponseDto>(response);
                    string validationError;
                    if (!TryAcceptPreview(parsed, envelope, out validationError))
                    {
                        throw new InvalidOperationException(validationError);
                    }
                    pendingChangeSet = parsed.ChangeSet.Executable ? parsed.ChangeSet : null;
                    control.SetPendingChangeSet(pendingChangeSet != null);
                    control.SetResponse(response);
                    control.SetStatus(
                        pendingChangeSet == null
                            ? "preview received; no executable operations"
                            : "preview ready; review and confirm before Apply",
                        false);
                },
                false);
        }

        private void ApplyRequested(object sender, EventArgs args)
        {
            if (pendingChangeSet == null || !pendingChangeSet.Executable)
            {
                control.SetStatus("no executable ChangeSet is pending", true);
                return;
            }
            if (!EnsureCurrentSelection()) { return; }
            if (!String.Equals(
                currentEnvelope.Selection.FullName,
                pendingChangeSet.TargetElement,
                StringComparison.Ordinal))
            {
                pendingChangeSet = null;
                control.SetPendingChangeSet(false);
                control.SetStatus("Current Element changed; preview again", true);
                return;
            }

            bool persistRequested = control.GetPersistRequested();
            DialogResult decision = MessageBox.Show(
                control,
                BuildConfirmation(pendingChangeSet, persistRequested),
                "Confirm controlled E3D change",
                MessageBoxButtons.OKCancel,
                MessageBoxIcon.Warning,
                MessageBoxDefaultButton.Button2);
            if (decision != DialogResult.OK)
            {
                control.SetStatus("Apply cancelled by operator", false);
                return;
            }

            ChangeSetDto changeSet = pendingChangeSet;
            SelectionEnvelopeDto envelope = currentEnvelope;
            BridgeConfiguration configuration = currentConfiguration;
            ApplyAuthorizationRequestDto request = ApplyAuthorizationRequestDto.Create(
                envelope,
                changeSet,
                persistRequested);
            RunGatewayCall(
                configuration,
                delegate(GatewayClient client) { return client.PostApplyAuthorization(request); },
                delegate(string response)
                {
                    ApplyAuthorizationResponseDto authorization =
                        JsonCodec.Deserialize<ApplyAuthorizationResponseDto>(response);
                    isApplying = true;
                    ApplyResultRequestDto result;
                    try
                    {
                        result = ControlledChangeExecutor.Execute(
                            configuration,
                            envelope,
                            authorization);
                    }
                    finally
                    {
                        isApplying = false;
                    }

                    pendingChangeSet = null;
                    control.SetPendingChangeSet(false);
                    control.SetResponse(JsonCodec.Serialize(result));
                    control.SetStatus(
                        "apply finished: " + result.Status + " / " + result.Persistence,
                        result.Status != "applied");
                    CaptureCurrentSelection(false);

                    RunGatewayCall(
                        configuration,
                        delegate(GatewayClient client) { return client.PostApplyResult(result); },
                        delegate(string receipt)
                        {
                            control.SetStatus(
                                "execution receipt recorded: " + result.Status,
                                result.Status != "applied");
                        },
                        false);
                },
                false);
        }

        private bool EnsureCurrentSelection()
        {
            if (currentConfiguration == null || currentEnvelope == null)
            {
                CaptureCurrentSelection(false);
            }
            return currentConfiguration != null && currentEnvelope != null;
        }

        private static bool TryAcceptPreview(
            ChangePreviewResponseDto preview,
            SelectionEnvelopeDto envelope,
            out string error)
        {
            error = String.Empty;
            if (preview == null || preview.ProtocolVersion != BridgeConstants.ProtocolVersion ||
                preview.Status != "preview_ready" || preview.ChangeSet == null ||
                preview.ChangeSet.Scope == null || preview.ChangeSet.Operations == null)
            {
                error = "Gateway returned an invalid preview response.";
                return false;
            }
            if (!SelectionSnapshotBuilder.ScopesMatch(
                preview.ChangeSet.Scope,
                envelope.Session.Scope) ||
                !String.Equals(
                    preview.ChangeSet.TargetElement,
                    envelope.Selection.FullName,
                    StringComparison.Ordinal))
            {
                error = "Preview scope or target does not match the current selection.";
                return false;
            }
            if (preview.ChangeSet.Executable &&
                (String.IsNullOrWhiteSpace(preview.ChangeSet.ChangeSetId) ||
                    preview.ChangeSet.Operations.Count == 0 ||
                    preview.ChangeSet.Operations.Count > 16))
            {
                error = "Executable preview is missing a bounded ChangeSet.";
                return false;
            }
            foreach (PreviewOperationDto operation in preview.ChangeSet.Operations)
            {
                if (operation == null || !String.Equals(
                    operation.TargetElement,
                    envelope.Selection.FullName,
                    StringComparison.Ordinal))
                {
                    error = "Preview contains a cross-element operation.";
                    return false;
                }
            }
            return true;
        }

        private static string BuildConfirmation(ChangeSetDto changeSet, bool persistRequested)
        {
            StringBuilder text = new StringBuilder();
            text.AppendLine("Target: " + changeSet.TargetElement);
            text.AppendLine("ChangeSet: " + changeSet.ChangeSetId);
            text.AppendLine();
            foreach (PreviewOperationDto operation in changeSet.Operations)
            {
                text.AppendLine(
                    operation.Attribute + ": " + operation.ExpectedCurrentValue +
                    " -> " + operation.ProposedValue);
            }
            text.AppendLine();
            text.AppendLine(
                persistRequested
                    ? "The verified transaction will be followed by Save Work."
                    : "The verified transaction will remain in memory until you Save Work.");
            text.Append("Click OK only after reviewing every operation.");
            return text.ToString();
        }

        private void RunGatewayCall(
            BridgeConfiguration configuration,
            Func<GatewayClient, string> action,
            Action<string> onSuccess,
            bool displayRawResponse)
        {
            int sequence = Interlocked.Increment(ref requestSequence);
            control.SetBusy(true);
            control.SetStatus("contacting isolated gateway", false);
            Task.Factory.StartNew(delegate
            {
                return action(new GatewayClient(configuration));
            }).ContinueWith(delegate(Task<string> task)
            {
                if (control == null || control.IsDisposed || sequence != requestSequence)
                {
                    return;
                }
                control.BeginInvoke(new Action(delegate
                {
                    control.SetBusy(false);
                    if (task.IsFaulted)
                    {
                        Exception failure = task.Exception.GetBaseException();
                        control.SetStatus("gateway error: " + failure.Message, true);
                    }
                    else if (task.IsCanceled)
                    {
                        control.SetStatus("gateway request cancelled", true);
                    }
                    else
                    {
                        try
                        {
                            if (displayRawResponse) { control.SetResponse(task.Result); }
                            if (onSuccess != null) { onSuccess(task.Result); }
                            else { control.SetStatus("gateway response received", false); }
                        }
                        catch (Exception failure)
                        {
                            pendingChangeSet = null;
                            control.SetPendingChangeSet(false);
                            control.SetStatus(
                                "response validation failed: " + failure.Message,
                                true);
                        }
                    }
                }));
            });
        }
    }
}
