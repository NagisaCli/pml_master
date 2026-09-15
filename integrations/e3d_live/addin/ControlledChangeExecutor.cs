using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text.RegularExpressions;
using Aveva.Core.Database;
using Aveva.Core.Utilities.Undo;

namespace E3DLiveBridge.Addin
{
    internal static class ControlledChangeExecutor
    {
        private static readonly HashSet<string> ExecutableAttributes =
            new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            {
                "DESC", "XLEN", "YLEN", "ZLEN", "HEIG", "DIAM", "DTOP", "DBOT"
            };

        private static readonly Regex NumericValue = new Regex(
            @"^(?<value>(?:0|[1-9][0-9]*)(?:\.[0-9]+)?)\s*(?<unit>mm|m)?$",
            RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);

        private sealed class PreparedOperation
        {
            internal PreviewOperationDto Source;
            internal DbAttribute Attribute;
            internal string StringValue;
            internal double NumericValue;
            internal bool IsString;
            internal string BeforeValue;
        }

        internal static ApplyResultRequestDto Execute(
            BridgeConfiguration configuration,
            SelectionEnvelopeDto envelope,
            ApplyAuthorizationResponseDto authorization)
        {
            string validationError;
            List<PreparedOperation> prepared;
            if (!TryPrepare(configuration, envelope, authorization, out prepared, out validationError))
            {
                return BuildResult(
                    envelope,
                    authorization,
                    validationError.IndexOf("precondition", StringComparison.OrdinalIgnoreCase) >= 0
                        ? "stale"
                        : "rejected",
                    "none",
                    validationError,
                    new List<ApplyOperationResultDto>());
            }

            UndoTransaction transaction = UndoTransaction.GetUndoTransaction();
            bool transactionStarted = false;
            List<ApplyOperationResultDto> results = new List<ApplyOperationResultDto>();
            try
            {
                transaction.StartTransaction(
                    "E3D AI controlled change " + authorization.ChangeSetId);
                transactionStarted = true;
                DbElement element = DbElement.GetElement(authorization.TargetElement);

                foreach (PreparedOperation item in prepared)
                {
                    if (item.IsString)
                    {
                        element.SetAttribute(item.Attribute, item.StringValue);
                    }
                    else
                    {
                        element.SetAttribute(item.Attribute, item.NumericValue);
                    }
                    string afterValue = element.GetAsString(item.Attribute);
                    if (!ReadbackMatches(item.Source, afterValue))
                    {
                        throw new InvalidOperationException(
                            "readback mismatch for " + item.Source.Attribute +
                            ": requested '" + item.Source.ProposedValue +
                            "', received '" + afterValue + "'");
                    }
                    results.Add(new ApplyOperationResultDto
                    {
                        OperationId = item.Source.OperationId,
                        Attribute = item.Source.Attribute,
                        BeforeValue = item.BeforeValue,
                        RequestedValue = item.Source.ProposedValue,
                        AfterValue = afterValue,
                        Status = "applied"
                    });
                }

                transaction.EndTransaction();
                transactionStarted = false;

                if (authorization.PersistRequested)
                {
                    try
                    {
                        MDB.CurrentMDB.SaveWork(
                            "E3D AI controlled change " + authorization.ChangeSetId);
                    }
                    catch (Exception saveFailure)
                    {
                        return BuildResult(
                            envelope,
                            authorization,
                            "applied_not_persisted",
                            "in_memory",
                            "Attributes were applied and verified, but Save Work failed: " +
                                saveFailure.Message,
                            results);
                    }
                }

                return BuildResult(
                    envelope,
                    authorization,
                    "applied",
                    authorization.PersistRequested ? "save_work" : "in_memory",
                    "All operations were applied and independently read back.",
                    results);
            }
            catch (Exception failure)
            {
                bool rolledBack = false;
                string rollbackMessage = String.Empty;
                if (transactionStarted)
                {
                    try
                    {
                        transaction.AbortTransaction();
                        rolledBack = true;
                    }
                    catch (Exception rollbackFailure)
                    {
                        rollbackMessage = "; rollback also failed: " + rollbackFailure.Message;
                    }
                }
                foreach (ApplyOperationResultDto result in results)
                {
                    result.Status = rolledBack ? "rolled_back" : "failed";
                }
                return BuildResult(
                    envelope,
                    authorization,
                    rolledBack ? "rolled_back" : "failed",
                    "none",
                    "Controlled transaction failed: " + failure.Message + rollbackMessage,
                    results);
            }
        }

        private static bool TryPrepare(
            BridgeConfiguration configuration,
            SelectionEnvelopeDto envelope,
            ApplyAuthorizationResponseDto authorization,
            out List<PreparedOperation> prepared,
            out string error)
        {
            prepared = new List<PreparedOperation>();
            error = String.Empty;
            if (configuration == null || !configuration.WriteEnabled ||
                !String.Equals(
                    configuration.AccessMode,
                    BridgeConstants.ControlledWriteMode,
                    StringComparison.Ordinal))
            {
                error = "The active PID-scoped session is not write-enabled.";
                return false;
            }
            if (authorization == null ||
                authorization.ProtocolVersion != BridgeConstants.ProtocolVersion ||
                authorization.Status != "authorized" ||
                String.IsNullOrWhiteSpace(authorization.AuthorizationId) ||
                authorization.Operations == null || authorization.Operations.Count == 0 ||
                authorization.Operations.Count > 16)
            {
                error = "The gateway authorization is missing or invalid.";
                return false;
            }
            DateTime expiresAt;
            if (!DateTime.TryParse(
                authorization.ExpiresAtUtc,
                CultureInfo.InvariantCulture,
                DateTimeStyles.AdjustToUniversal | DateTimeStyles.AssumeUniversal,
                out expiresAt) || expiresAt.ToUniversalTime() <= DateTime.UtcNow)
            {
                error = "The gateway authorization has expired.";
                return false;
            }
            ScopeDto actualScope = SelectionSnapshotBuilder.ReadActualScope();
            if (!SelectionSnapshotBuilder.ScopesMatch(configuration.ExpectedScope, actualScope) ||
                !SelectionSnapshotBuilder.ScopesMatch(authorization.Scope, actualScope))
            {
                error = "The live E3D scope no longer matches the authorized scope.";
                return false;
            }

            DbElement current = CurrentElement.Element;
            if (current == null || !current.IsValid)
            {
                error = "The E3D Current Element is invalid.";
                return false;
            }
            string currentName = SelectionSnapshotBuilder.ReadFullName(current);
            if (!String.Equals(currentName, authorization.TargetElement, StringComparison.Ordinal) ||
                !String.Equals(currentName, envelope.Selection.FullName, StringComparison.Ordinal))
            {
                error = "The Current Element changed after the preview.";
                return false;
            }
            DbElement target = DbElement.GetElement(authorization.TargetElement);
            if (target == null || !target.IsValid ||
                !String.Equals(
                    SelectionSnapshotBuilder.ReadFullName(target),
                    authorization.TargetElement,
                    StringComparison.Ordinal))
            {
                error = "The authorized target element cannot be resolved exactly.";
                return false;
            }

            HashSet<string> attributes = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (PreviewOperationDto operation in authorization.Operations)
            {
                if (operation == null || operation.OperationType != "set_attribute" ||
                    !String.Equals(
                        operation.TargetElement,
                        authorization.TargetElement,
                        StringComparison.Ordinal))
                {
                    error = "The authorization contains an unsupported operation.";
                    return false;
                }
                string attributeName = (operation.Attribute ?? String.Empty).ToUpperInvariant();
                if (!ExecutableAttributes.Contains(attributeName) || !attributes.Add(attributeName))
                {
                    error = "The authorization contains a non-allowlisted or duplicate attribute.";
                    return false;
                }
                DbAttribute attribute = DbAttribute.GetDbAttribute(attributeName);
                if (attribute == null || !attribute.IsValid)
                {
                    error = "The authorized attribute is invalid in E3D: " + attributeName;
                    return false;
                }
                string beforeValue = target.GetAsString(attribute);
                if (!String.Equals(
                    beforeValue,
                    operation.ExpectedCurrentValue,
                    StringComparison.Ordinal))
                {
                    error = "A stale precondition blocked " + attributeName +
                        ": expected '" + operation.ExpectedCurrentValue +
                        "', live value is '" + beforeValue + "'.";
                    return false;
                }

                string stringValue;
                double numericValue;
                bool isString;
                if (!TryConvertValue(
                    attributeName,
                    operation.ProposedValue,
                    out stringValue,
                    out numericValue,
                    out isString,
                    out error))
                {
                    return false;
                }
                prepared.Add(new PreparedOperation
                {
                    Source = operation,
                    Attribute = attribute,
                    StringValue = stringValue,
                    NumericValue = numericValue,
                    IsString = isString,
                    BeforeValue = beforeValue
                });
            }
            return true;
        }

        private static bool TryConvertValue(
            string attribute,
            string proposed,
            out string stringValue,
            out double numericValue,
            out bool isString,
            out string error)
        {
            stringValue = null;
            numericValue = 0.0;
            isString = false;
            error = String.Empty;
            if (attribute == "DESC")
            {
                if (String.IsNullOrWhiteSpace(proposed) || proposed.Length > 256)
                {
                    error = "DESC must contain 1 to 256 characters.";
                    return false;
                }
                foreach (char character in proposed)
                {
                    if (Char.IsControl(character))
                    {
                        error = "DESC cannot contain control characters.";
                        return false;
                    }
                }
                stringValue = proposed;
                isString = true;
                return true;
            }

            double millimetres;
            if (!TryParseMillimetres(proposed, out millimetres) ||
                millimetres <= 0.0 || millimetres > 100000000.0)
            {
                error = attribute +
                    " must be a positive number optionally followed by mm or m.";
                return false;
            }
            numericValue = millimetres;
            return true;
        }

        private static bool ReadbackMatches(PreviewOperationDto operation, string actual)
        {
            if (String.Equals(operation.Attribute, "DESC", StringComparison.OrdinalIgnoreCase))
            {
                return String.Equals(operation.ProposedValue, actual, StringComparison.Ordinal);
            }
            double expected;
            double observed;
            return TryParseMillimetres(operation.ProposedValue, out expected) &&
                TryParseMillimetres(actual, out observed) &&
                Math.Abs(expected - observed) <= Math.Max(0.001, Math.Abs(expected) * 0.000001);
        }

        private static bool TryParseMillimetres(string text, out double value)
        {
            value = 0.0;
            Match match = NumericValue.Match((text ?? String.Empty).Trim());
            if (!match.Success || !Double.TryParse(
                match.Groups["value"].Value,
                NumberStyles.AllowDecimalPoint,
                CultureInfo.InvariantCulture,
                out value))
            {
                return false;
            }
            if (String.Equals(match.Groups["unit"].Value, "m", StringComparison.OrdinalIgnoreCase))
            {
                value *= 1000.0;
            }
            return true;
        }

        private static ApplyResultRequestDto BuildResult(
            SelectionEnvelopeDto envelope,
            ApplyAuthorizationResponseDto authorization,
            string status,
            string persistence,
            string message,
            List<ApplyOperationResultDto> results)
        {
            return new ApplyResultRequestDto
            {
                ProtocolVersion = BridgeConstants.ProtocolVersion,
                MessageType = "apply_result",
                RequestId = Guid.NewGuid().ToString("D"),
                TimestampUtc = DateTime.UtcNow.ToString("o"),
                Session = envelope.Session,
                AuthorizationId = authorization.AuthorizationId,
                ChangeSetId = authorization.ChangeSetId,
                TargetElement = authorization.TargetElement,
                Status = status,
                Persistence = persistence,
                Message = message,
                OperationResults = results
            };
        }
    }
}
