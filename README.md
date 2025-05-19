# Backend Order Management API (.NET 8)

This project is a .NET 8 Web API for managing orders, parties, services, charges, deposits, loans, and fees. It uses RESTful conventions and in-memory storage for simplicity.

## Features
- Create, get, update, and delete orders
- Add/update/delete parties (buyer, seller, lender, attorney) to orders
- Add/update/delete services (Escrow, Title)
- Add/update/delete charges, deposits, loans, fees

## Endpoints (to be implemented)
- `POST /orders` - Create a new order (organization, serviceType required)
- `GET /orders/{id}` - Get order by ID
- `DELETE /orders/{id}` - Delete order
- `PUT /orders/{id}/parties/{partyType}` - Add/update a party
- `PUT /orders/{id}/services` - Add/update a service
- `PUT /orders/{id}/charges` - Add/update a charge
- `PUT /orders/{id}/deposits` - Add/update a deposit
- `PUT /orders/{id}/loans` - Add/update a loan
- `PUT /orders/{id}/fees` - Add/update a fee

## How to Run

```zsh
dotnet run
```

The API will be available at `https://localhost:5001` or `http://localhost:5000` by default.

---

This project is scaffolded for further development. See `.github/copilot-instructions.md` for Copilot customization.
