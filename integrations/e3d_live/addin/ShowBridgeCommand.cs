using System;
using Aveva.ApplicationFramework;
using Aveva.ApplicationFramework.Presentation;

namespace E3DLiveBridge.Addin
{
    internal sealed class ShowBridgeCommand : Command
    {
        private readonly DockedWindow window;

        internal ShowBridgeCommand(DockedWindow window)
        {
            Key = "E3DLiveBridge.ShowPanel";
            this.window = window;
            window.Closed += WindowClosed;
            DependencyResolver.GetImplementationOf<IWindowManager>().WindowLayoutLoaded +=
                WindowLayoutLoaded;
            window.Show();
            Checked = true;
        }

        public override void Execute()
        {
            if (Checked)
            {
                window.Show();
            }
            else
            {
                window.Hide();
            }
        }

        private void WindowClosed(object sender, EventArgs args)
        {
            Checked = false;
        }

        private void WindowLayoutLoaded(object sender, EventArgs args)
        {
            // Experimental bridge must remain discoverable even when a saved
            // workspace layout predates this docked window.
            window.Show();
            Checked = true;
        }
    }
}
