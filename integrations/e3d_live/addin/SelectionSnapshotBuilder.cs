using System;
using System.Collections.Generic;
using System.Diagnostics;
using Aveva.Core.Database;

namespace E3DLiveBridge.Addin
{
    internal static class SelectionSnapshotBuilder
    {
        private static readonly string[] AttributeAllowlist = new string[]
        {
            "NAME", "DESC", "POS", "ORI", "XLEN", "YLEN", "ZLEN",
            "HEIG", "DIAM", "DTOP", "DBOT", "CATR", "BORD", "PRES",
            "TEMP"
        };

        internal static bool TryBuild(
            BridgeConfiguration configuration,
            out SelectionEnvelopeDto envelope,
            out string error)
        {
            envelope = null;
            error = String.Empty;
            try
            {
                ScopeDto actualScope = ReadActualScope();
                if (!ScopesMatch(configuration.ExpectedScope, actualScope))
                {
                    error = "Scope rejected. Gateway=" +
                        configuration.ExpectedScope.DisplayName + ", E3D=" +
                        actualScope.DisplayName;
                    return false;
                }

                DbElement element = CurrentElement.Element;
                if (element == null || !element.IsValid)
                {
                    error = "E3D current element is not valid.";
                    return false;
                }

                envelope = new SelectionEnvelopeDto
                {
                    ProtocolVersion = BridgeConstants.ProtocolVersion,
                    MessageType = "selection_snapshot",
                    RequestId = Guid.NewGuid().ToString("D"),
                    TimestampUtc = DateTime.UtcNow.ToString("o"),
                    Session = new SessionDto
                    {
                        BridgeSessionId = configuration.BridgeSessionId,
                        ProcessId = Process.GetCurrentProcess().Id,
                        Source = BridgeConstants.Source,
                        AddinVersion = BridgeConstants.AddinVersion,
                        Scope = actualScope
                    },
                    Selection = new SelectionDto
                    {
                        FullName = ReadFullName(element),
                        ElementType = element.GetActualType().Name,
                        OwnerFullName = ReadOwnerFullName(element),
                        Attributes = ReadAllowlistedAttributes(element)
                    }
                };
                return true;
            }
            catch (Exception exception)
            {
                error = "Unable to snapshot the current element: " + exception.Message;
                return false;
            }
        }

        internal static ScopeDto ReadActualScope()
        {
            return new ScopeDto
            {
                ProjectCode = BridgeConfiguration.Normalise(Project.CurrentProject.Code),
                Mdb = BridgeConfiguration.Normalise(MDB.CurrentMDB.Name),
                Module = "DESIGN"
            };
        }

        internal static bool ScopesMatch(ScopeDto expected, ScopeDto actual)
        {
            return String.Equals(expected.ProjectCode, actual.ProjectCode, StringComparison.Ordinal) &&
                String.Equals(expected.Mdb, actual.Mdb, StringComparison.Ordinal) &&
                String.Equals(expected.Module, actual.Module, StringComparison.Ordinal);
        }

        internal static string ReadFullName(DbElement element)
        {
            return element.GetAsString(DbAttributeInstance.FLNM);
        }

        private static string ReadOwnerFullName(DbElement element)
        {
            try
            {
                DbElement owner = element.Owner;
                if (owner != null && owner.IsValid)
                {
                    return ReadFullName(owner);
                }
            }
            catch
            {
                // The root element has no owner; return an empty value.
            }
            return String.Empty;
        }

        private static Dictionary<string, string> ReadAllowlistedAttributes(DbElement element)
        {
            Dictionary<string, string> values = new Dictionary<string, string>(
                StringComparer.OrdinalIgnoreCase);
            foreach (string attributeName in AttributeAllowlist)
            {
                try
                {
                    DbAttribute attribute = DbAttribute.GetDbAttribute(attributeName);
                    if (attribute != null && attribute.IsValid)
                    {
                        values[attributeName] = element.GetAsString(attribute);
                    }
                }
                catch
                {
                    // Attributes that are invalid for this element type are omitted.
                }
            }
            return values;
        }
    }
}
