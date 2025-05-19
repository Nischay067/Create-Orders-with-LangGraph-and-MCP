using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Gateway.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ChatController : ControllerBase
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _configuration;

        public ChatController(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClientFactory = httpClientFactory;
            _configuration = configuration;
        }

        [HttpPost]
        public async Task<IActionResult> Post([FromBody] ChatRequest request)
        {
            // Forward the chat message to the agentic AI layer (LangGraph)
            var langGraphUrl = _configuration["LangGraph:Endpoint"];
            if (string.IsNullOrWhiteSpace(langGraphUrl))
                return StatusCode(500, "LangGraph endpoint is not configured.");

            var client = _httpClientFactory.CreateClient();
            var content = new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json");
            var response = await client.PostAsync(langGraphUrl, content);
            var responseBody = await response.Content.ReadAsStringAsync();
            return Content(responseBody, response.Content.Headers.ContentType?.ToString() ?? "application/json");
        }
    }

    public class ChatRequest
    {
        public string message { get; set; } = string.Empty;
        public string? userId { get; set; }
    }
}
