using System;
using System.Threading.Tasks;
using Azure;
using Azure.AI.OpenAI;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

namespace RGKTestOpenAI
{
    //GPT4 calls

        class Program
        {               
                static void Main(string[] args)
                {

            string apiKey, apiUrl;

            Console.WriteLine($"Start Time : {DateTime.Now}");
            
            GetSecrets(out apiKey, out apiUrl);


            #region

            // Fetch the API key from an environment variable
            // string apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");

            if (string.IsNullOrEmpty(apiKey))
            {
                Console.WriteLine("Error: OPENAI_API_KEY variable is not accessible from Key Vault.");
                return;
            }

            if (string.IsNullOrEmpty(apiUrl))
            {
                Console.WriteLine("Error: OPENAI_API_Url variable is not accessible from Key Vault.");
                return;
            }

            Uri azureOpenAIResourceUri = new Uri(apiUrl);

            // Uri azureOpenAIResourceUri = new Uri(Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT"));
            Azure.AzureKeyCredential azureOpenAIApiKey = new AzureKeyCredential(apiKey);

            // Create an instance of the OpenAIClient
            OpenAIClient client = new OpenAIClient(azureOpenAIResourceUri, azureOpenAIApiKey);

            // Example: Chat completion
            var chatCompletionsOptions = new ChatCompletionsOptions()
            {
                DeploymentName = "depl-gpt-4", // Use DeploymentName for "model" with non-Azure clients
                Messages =
                        {
                        // The system message represents instructions or other guidance about how the assistant should behave
                        new ChatRequestSystemMessage("You are a helpful assistant."),
                        new ChatRequestUserMessage("Who is lord krishna in 5 words?")
                        }
            };

            Response<ChatCompletions> chatCompletionResponse = client.GetChatCompletions(chatCompletionsOptions);

            // Access the model-generated message
            if (chatCompletionResponse.Value.Choices.Count > 0)
            {
                var modelResponse = chatCompletionResponse.Value.Choices[0].Message.Content.ToString();
                Console.WriteLine("Model response >>> : " + modelResponse);
            }
            else
            {
                Console.WriteLine("No model-generated message received.");
            }

            Console.WriteLine($"End Time : {DateTime.Now}");

            static void GetSecrets(out string apiKey, out string apiUrl)
            {
                // Replace with your actual key vault URL
                var keyVaultUrl = new Uri("https://entagiliy-kv-openai-key.vault.azure.net/");
                var credential = new DefaultAzureCredential();

                var secretClient = new SecretClient(keyVaultUrl, credential);
                KeyVaultSecret apiKeyKeySecret = secretClient.GetSecret("EntAgility-OpenAI-Secret-Key");
                KeyVaultSecret apiKeyUrlSecret = secretClient.GetSecret("EntAgility-OpenAI-Secret-Url");

                // Use apiKeySecret.Value in your application
                apiKey = apiKeyKeySecret.Value;
                apiUrl = apiKeyUrlSecret.Value;
            }

            #endregion

        }

    }
}


/*


Azure OpenAI Nuget Package in .NET C# in VSCode:
dotnet add package Azure.AI.OpenAI --version 1.0.0-beta.13


Azure OpenAI Nuget Package in .NET C# in Visual Studio 2019:
Usage: dotnet add <PROJECT> package  Azure.AI.OpenAI --version 1.0.0-beta.13
Actual Command: dotnet add RGKTestOpenAI(project name) package  Azure.AI.OpenAI --version 1.0.0-beta.13
Instruction: run from package manager console 


To access Azure Key Vault from Python below is the pip install package:
pip install azure-identity azure-keyvault-secrets
*/
