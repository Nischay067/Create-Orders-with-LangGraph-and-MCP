using Microsoft.AspNetCore.Mvc;
using System.Collections.Concurrent;

// Models
public record Order(
    int Id,
    string Organization,
    string TransactionType, // Type: Sale with Mortgage, Refinance, Sale with Cash, etc.
    List<Party>? Parties = null,
    List<Service>? Services = null,
    List<Charge>? Charges = null,
    List<Deposit>? Deposits = null,
    List<Loan>? Loans = null,
    List<Fee>? Fees = null
);

public record Party(string Type, string Name); // Type: buyer/seller/lender/attorney
public record Service(string Type); // Type: Escrow/Title/Both
public record Charge(string Description, decimal Amount);
public record Deposit(string Description, decimal Amount);
public record Loan(string Lender, decimal Amount);
public record Fee(string Description, decimal Amount);

[ApiController]
[Route("[controller]")]
public class OrdersController : ControllerBase
{
    // In-memory storage
    private static readonly ConcurrentDictionary<int, Order> Orders = new();
    private static int _orderIdSeed = 4999;

    // POST /orders
    [HttpPost]
    public IActionResult CreateOrder([FromBody] CreateOrderRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Organization) || string.IsNullOrWhiteSpace(request.TransactionType))
            return BadRequest("Organization and TransactionType are required.");
        // Use an incrementing int for Id, starting from 5000
        var orderId = System.Threading.Interlocked.Increment(ref _orderIdSeed);
        var order = new Order(
            orderId,
            request.Organization,
            request.TransactionType,
            request.Parties,
            request.Services,
            request.Charges,
            request.Deposits,
            request.Loans,
            request.Fees
        );
        Orders[order.Id] = order;
        return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order);
    }

    // GET /orders/{id}
    [HttpGet("{id}")]
    public IActionResult GetOrder(int id)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        return Ok(order);
    }

    // DELETE /orders/{id}
    [HttpDelete("{id}")]
    public IActionResult DeleteOrder(int id)
    {
        if (!Orders.TryRemove(id, out _))
            return NotFound();
        return NoContent();
    }

    // PUT /orders/{id}/services
    [HttpPut("{id}/services")]
    public IActionResult AddOrUpdateService(int id, [FromBody] Service service)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        var services = order.Services ?? new List<Service>();
        services.RemoveAll(s => s.Type.Equals(service.Type, StringComparison.OrdinalIgnoreCase));
        services.Add(service);
        Orders[id] = order with { Services = services };
        return Ok(Orders[id]);
    }

    // PUT /orders/{id}/parties/{partyType}
    [HttpPut("{id}/parties/{partyType}")]
    public IActionResult AddOrUpdateParty(int id, string partyType, [FromBody] Party party)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        var parties = order.Parties ?? new List<Party>();
        parties.RemoveAll(p => p.Type.Equals(partyType, StringComparison.OrdinalIgnoreCase));
        parties.Add(party);
        Orders[id] = order with { Parties = parties };
        return Ok(Orders[id]);
    }

    // PUT /orders/{id}/charges
    [HttpPut("{id}/charges")]
    public IActionResult AddOrUpdateCharge(int id, [FromBody] Charge charge)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        var charges = order.Charges ?? new List<Charge>();
        charges.RemoveAll(c => c.Description.Equals(charge.Description, StringComparison.OrdinalIgnoreCase));
        charges.Add(charge);
        Orders[id] = order with { Charges = charges };
        return Ok(Orders[id]);
    }

    // PUT /orders/{id}/deposits
    [HttpPut("{id}/deposits")]
    public IActionResult AddOrUpdateDeposit(int id, [FromBody] Deposit deposit)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        var deposits = order.Deposits ?? new List<Deposit>();
        deposits.RemoveAll(d => d.Description.Equals(deposit.Description, StringComparison.OrdinalIgnoreCase));
        deposits.Add(deposit);
        Orders[id] = order with { Deposits = deposits };
        return Ok(Orders[id]);
    }

    // PUT /orders/{id}/loans
    [HttpPut("{id}/loans")]
    public IActionResult AddOrUpdateLoan(int id, [FromBody] Loan loan)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        var loans = order.Loans ?? new List<Loan>();
        loans.RemoveAll(l => l.Lender.Equals(loan.Lender, StringComparison.OrdinalIgnoreCase));
        loans.Add(loan);
        Orders[id] = order with { Loans = loans };
        return Ok(Orders[id]);
    }

    // PUT /orders/{id}/fees
    [HttpPut("{id}/fees")]
    public IActionResult AddOrUpdateFee(int id, [FromBody] Fee fee)
    {
        if (!Orders.TryGetValue(id, out var order))
            return NotFound();
        var fees = order.Fees ?? new List<Fee>();
        fees.RemoveAll(f => f.Description.Equals(fee.Description, StringComparison.OrdinalIgnoreCase));
        fees.Add(fee);
        Orders[id] = order with { Fees = fees };
        return Ok(Orders[id]);
    }

    // GET /orders
    [HttpGet]
    public IActionResult GetAllOrders()
    {
        return Ok(Orders.Values);
    }
}

public class CreateOrderRequest
{
    public string Organization { get; set; } = string.Empty;
    public string TransactionType { get; set; } = string.Empty;
    public List<Party>? Parties { get; set; }
    public List<Service>? Services { get; set; }
    public List<Charge>? Charges { get; set; }
    public List<Deposit>? Deposits { get; set; }
    public List<Loan>? Loans { get; set; }
    public List<Fee>? Fees { get; set; }
}
