using System;
using System.IO;
using System.Net;
using System.Text;

namespace E3DLiveBridge.Addin
{
    internal sealed class GatewayClient
    {
        private readonly BridgeConfiguration configuration;

        internal GatewayClient(BridgeConfiguration configuration)
        {
            this.configuration = configuration;
        }

        internal string GetHealth()
        {
            Uri endpoint = new Uri(configuration.GatewayBaseUri, "health");
            HttpWebRequest request = CreateRequest(endpoint, "GET");
            return ReadResponse(request);
        }

        internal string PostSelection(SelectionEnvelopeDto envelope)
        {
            return PostJson("v1/selection", envelope, 10000);
        }

        internal string PostPreview(ChangePreviewRequestDto preview)
        {
            return PostJson("v1/preview", preview, 90000);
        }

        internal string PostConfigureAssistant(ConfigureAssistantRequestDto request)
        {
            return PostJson("v1/configure/assistant", request, 10000);
        }

        internal string PostApplyAuthorization(ApplyAuthorizationRequestDto request)
        {
            return PostJson("v1/apply/authorize", request, 10000);
        }

        internal string PostApplyResult(ApplyResultRequestDto request)
        {
            return PostJson("v1/apply/result", request, 10000);
        }

        private string PostJson<T>(string relativePath, T value, int timeoutMilliseconds)
        {
            Uri endpoint = new Uri(configuration.GatewayBaseUri, relativePath);
            HttpWebRequest request = CreateRequest(endpoint, "POST", timeoutMilliseconds);
            request.ContentType = "application/json; charset=utf-8";
            byte[] body = Encoding.UTF8.GetBytes(JsonCodec.Serialize(value));
            request.ContentLength = body.Length;
            using (Stream stream = request.GetRequestStream())
            {
                stream.Write(body, 0, body.Length);
            }
            return ReadResponse(request);
        }

        private HttpWebRequest CreateRequest(
            Uri endpoint,
            string method,
            int timeoutMilliseconds = 5000)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(endpoint);
            request.Method = method;
            request.Timeout = timeoutMilliseconds;
            request.ReadWriteTimeout = timeoutMilliseconds;
            request.Proxy = null;
            request.KeepAlive = false;
            request.Headers["X-E3D-Live-Token"] = configuration.Token;
            return request;
        }

        private static string ReadResponse(HttpWebRequest request)
        {
            try
            {
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                using (StreamReader reader = new StreamReader(response.GetResponseStream()))
                {
                    return reader.ReadToEnd();
                }
            }
            catch (WebException exception)
            {
                HttpWebResponse response = exception.Response as HttpWebResponse;
                if (response != null)
                {
                    using (response)
                    using (StreamReader reader = new StreamReader(response.GetResponseStream()))
                    {
                        throw new InvalidOperationException(
                            "Gateway returned " + (int)response.StatusCode + ": " +
                            reader.ReadToEnd(),
                            exception);
                    }
                }
                throw;
            }
        }
    }
}
