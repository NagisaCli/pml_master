using System;
using System.Drawing;
using System.Windows.Forms;

namespace E3DLiveBridge.Addin
{
    internal sealed class E3DLiveBridgeControl : UserControl
    {
        private readonly Label scopeLabel;
        private readonly Label statusLabel;
        private readonly TextBox selectionText;
        private readonly TextBox instructionText;
        private readonly TextBox apiKeyText;
        private readonly ComboBox providerCombo;
        private readonly TextBox endpointText;
        private readonly TextBox modelText;
        private readonly TextBox responseText;
        private readonly Button healthButton;
        private readonly Button sendButton;
        private readonly Button previewButton;
        private readonly Button configureButton;
        private readonly Button applyButton;
        private readonly CheckBox autoSendCheck;
        private readonly CheckBox persistCheck;
        private readonly Timer autoSendTimer;
        private bool hasPendingChangeSet;

        internal event EventHandler HealthRequested;
        internal event EventHandler SendRequested;
        internal event EventHandler PreviewRequested;
        internal event EventHandler ConfigureRequested;
        internal event EventHandler ApplyRequested;

        internal E3DLiveBridgeControl()
        {
            Dock = DockStyle.Fill;
            BackColor = SystemColors.Control;

            scopeLabel = new Label
            {
                AutoSize = true,
                Text = "Scope: not connected",
                Dock = DockStyle.Fill
            };
            statusLabel = new Label
            {
                AutoSize = true,
                Text = "CONTROLLED: waiting for PID-scoped gateway session",
                ForeColor = Color.DarkRed,
                Dock = DockStyle.Fill
            };
            selectionText = new TextBox
            {
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Both,
                WordWrap = false,
                Dock = DockStyle.Fill
            };
            responseText = new TextBox
            {
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical,
                Dock = DockStyle.Fill
            };
            instructionText = new TextBox
            {
                Multiline = true,
                ScrollBars = ScrollBars.Vertical,
                Dock = DockStyle.Fill
            };
            apiKeyText = new TextBox
            {
                UseSystemPasswordChar = true,
                Dock = DockStyle.Fill
            };
            providerCombo = new ComboBox
            {
                DropDownStyle = ComboBoxStyle.DropDownList,
                Dock = DockStyle.Fill
            };
            providerCombo.Items.Add("Token Rhythm (Chat Completions)");
            providerCombo.Items.Add("OpenAI (Responses)");
            providerCombo.SelectedIndex = 0;
            endpointText = new TextBox
            {
                ReadOnly = true,
                Text = "https://tokenrhythm.studio/v1",
                Dock = DockStyle.Fill
            };
            modelText = new TextBox
            {
                Text = "deepseek-v4-flash",
                Dock = DockStyle.Fill
            };
            healthButton = new Button { Text = "Check Gateway", AutoSize = true };
            sendButton = new Button { Text = "Send Selection", AutoSize = true };
            previewButton = new Button { Text = "Preview Changes", AutoSize = true };
            configureButton = new Button { Text = "Configure AI", AutoSize = true };
            applyButton = new Button
            {
                Text = "Apply Verified ChangeSet",
                AutoSize = true,
                Enabled = false
            };
            autoSendCheck = new CheckBox
            {
                Text = "Auto-send selection",
                AutoSize = true,
                Checked = true
            };
            persistCheck = new CheckBox
            {
                Text = "Save Work after verified apply",
                AutoSize = true,
                Checked = false
            };

            providerCombo.SelectedIndexChanged += delegate
            {
                if (providerCombo.SelectedIndex == 1)
                {
                    endpointText.Text = "https://api.openai.com/v1";
                    modelText.Text = "gpt-5.4-2026-03-05";
                }
                else
                {
                    endpointText.Text = "https://tokenrhythm.studio/v1";
                    modelText.Text = "deepseek-v4-flash";
                }
            };

            healthButton.Click += delegate { Raise(HealthRequested); };
            sendButton.Click += delegate { Raise(SendRequested); };
            previewButton.Click += delegate { Raise(PreviewRequested); };
            configureButton.Click += delegate { Raise(ConfigureRequested); };
            applyButton.Click += delegate { Raise(ApplyRequested); };
            autoSendTimer = new Timer { Interval = 400 };
            autoSendTimer.Tick += delegate
            {
                autoSendTimer.Stop();
                if (autoSendCheck.Checked)
                {
                    Raise(SendRequested);
                }
            };

            FlowLayoutPanel buttons = new FlowLayoutPanel
            {
                AutoSize = true,
                Dock = DockStyle.Fill,
                FlowDirection = FlowDirection.LeftToRight
            };
            buttons.Controls.Add(healthButton);
            buttons.Controls.Add(sendButton);
            buttons.Controls.Add(previewButton);
            buttons.Controls.Add(applyButton);
            buttons.Controls.Add(autoSendCheck);
            buttons.Controls.Add(persistCheck);

            FlowLayoutPanel apiButtons = new FlowLayoutPanel
            {
                AutoSize = true,
                Dock = DockStyle.Fill,
                FlowDirection = FlowDirection.LeftToRight
            };
            apiButtons.Controls.Add(configureButton);
            apiButtons.Controls.Add(new Label
            {
                Text = "Key stays in gateway memory only",
                AutoSize = true,
                Padding = new Padding(4, 6, 0, 0)
            });

            TableLayoutPanel providerLayout = new TableLayoutPanel
            {
                ColumnCount = 2,
                RowCount = 4,
                AutoSize = true,
                Dock = DockStyle.Fill
            };
            providerLayout.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));
            providerLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            providerLayout.Controls.Add(new Label
            {
                Text = "Provider",
                AutoSize = true,
                Padding = new Padding(0, 4, 4, 0)
            }, 0, 0);
            providerLayout.Controls.Add(providerCombo, 1, 0);
            providerLayout.Controls.Add(new Label
            {
                Text = "Endpoint",
                AutoSize = true,
                Padding = new Padding(0, 4, 4, 0)
            }, 0, 1);
            providerLayout.Controls.Add(endpointText, 1, 1);
            providerLayout.Controls.Add(new Label
            {
                Text = "Model ID",
                AutoSize = true,
                Padding = new Padding(0, 4, 4, 0)
            }, 0, 2);
            providerLayout.Controls.Add(modelText, 1, 2);
            providerLayout.Controls.Add(new Label
            {
                Text = "API key",
                AutoSize = true,
                Padding = new Padding(0, 4, 4, 0)
            }, 0, 3);
            providerLayout.Controls.Add(apiKeyText, 1, 3);

            TableLayoutPanel layout = new TableLayoutPanel
            {
                ColumnCount = 1,
                RowCount = 11,
                Dock = DockStyle.Fill,
                Padding = new Padding(6)
            };
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 48));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 70));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 52));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.Controls.Add(scopeLabel, 0, 0);
            layout.Controls.Add(statusLabel, 0, 1);
            layout.Controls.Add(new Label { Text = "Current selection", AutoSize = true }, 0, 2);
            layout.Controls.Add(selectionText, 0, 3);
            layout.Controls.Add(new Label { Text = "Change instruction", AutoSize = true }, 0, 4);
            layout.Controls.Add(instructionText, 0, 5);
            layout.Controls.Add(providerLayout, 0, 6);
            layout.Controls.Add(apiButtons, 0, 7);
            layout.Controls.Add(new Label { Text = "Gateway response / audit receipt", AutoSize = true }, 0, 8);
            layout.Controls.Add(responseText, 0, 9);
            layout.Controls.Add(buttons, 0, 10);
            Controls.Add(layout);
        }

        internal void SetScope(string scope)
        {
            scopeLabel.Text = "Scope: " + scope;
        }

        internal void SetStatus(string status, bool isError)
        {
            statusLabel.Text = "CONTROLLED: " + status;
            statusLabel.ForeColor = isError ? Color.DarkRed : Color.DarkGreen;
        }

        internal void SetSelection(SelectionEnvelopeDto envelope)
        {
            selectionText.Text = JsonCodec.Serialize(envelope);
            autoSendTimer.Stop();
            autoSendTimer.Start();
        }

        internal void SetResponse(string response)
        {
            responseText.Text = response;
        }

        internal string GetInstruction()
        {
            return instructionText.Text.Trim();
        }

        internal string TakeApiKey()
        {
            string value = apiKeyText.Text.Trim();
            apiKeyText.Clear();
            return value;
        }

        internal string GetAssistantProvider()
        {
            return providerCombo.SelectedIndex == 1
                ? "openai_responses"
                : "token_rhythm_chat";
        }

        internal string GetAssistantModel()
        {
            return modelText.Text.Trim();
        }

        internal bool GetPersistRequested()
        {
            return persistCheck.Checked;
        }

        internal void SetPendingChangeSet(bool available)
        {
            hasPendingChangeSet = available;
            applyButton.Enabled = available;
        }

        internal void SetBusy(bool busy)
        {
            healthButton.Enabled = !busy;
            sendButton.Enabled = !busy;
            previewButton.Enabled = !busy;
            configureButton.Enabled = !busy;
            applyButton.Enabled = !busy && hasPendingChangeSet;
        }

        private void Raise(EventHandler handler)
        {
            if (handler != null)
            {
                handler(this, EventArgs.Empty);
            }
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                autoSendTimer.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}
