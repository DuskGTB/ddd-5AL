
## Installation

```bash
git clone https://github.com/DuskGTB/ddd-5AL.git
cd ddd-5AL
```

---

## Commandes Docker

Lancer la base PostgreSQL et l’application :

```bash
docker-compose up -d --build
```

Exécuter la suite de tests :

```bash
docker-compose run --rm test
```

---

## API

- **POST** `/api/clients` — Créer un client  
- **POST** `/api/clients/{client_id}/wallet` — Créditer le wallet  
- **GET**  `/api/rooms` — Lister les types de chambres  
- **POST** `/api/reservations` — Créer une réservation  
- **POST** `/api/reservations/{reservation_id}/deposit` — Payer le dépôt (50 %)  
- **POST** `/api/reservations/{reservation_id}/confirm` — Confirmer (payer solde)  
- **POST** `/api/reservations/{reservation_id}/cancel` — Annuler  

(Voir fichier .http utilisable dans VScode via l'extension REST Client)
---

## Design stratégique

### 1. Ubiquitous Language

- **Client** : utilisateur du système, possède un portefeuille (`Wallet`)  
- **Wallet** : objet de valeur stockant un solde monétaire (`Money`)  
- **Reservation** : agrégat représentant la réservation d’une ou plusieurs chambres  
- **Room** : type de chambre (`standard`, `superior`, `suite`) avec prix et caractéristiques  
- **Money** : montant et devise (`EUR`, `USD`, …)  
- **ClientId / ReservationId** : identifiants forts (UUID)

### 2. Bounded Contexts


```mermaid
flowchart LR
  subgraph Client BC
    C[Client Management]
    W[Wallet Service]
  end
  subgraph Reservation BC
    R[Reservation Service]
    RM[Room Catalog]
  end
  subgraph Payment BC
    P[Deposit Payment]
    T[Top-Up Service]
  end

  R -->|query client| C
  R -->|compute deposit| P
  P -->|debit wallet| W
  T -->|credit wallet| W
```

### 3. Context Map


```mermaid
graph TD
  ReservationBC -->|reads| ClientBC
  ReservationBC -->|delegates deposit| PaymentBC
  PaymentBC -->|updates wallet| ClientBC
  ClientBC -.->|supports| Generic.Infrastructure
  ReservationBC -.->|uses| Generic.Infrastructure
  PaymentBC    -.->|uses| Generic.Infrastructure
```

### 4. Domain Classification

- **Core Domain**  
  - Reservation Service (gestion des réservations, calcul de montant, confirmation)  
- **Supporting Domain**  
  - Client Management (création de compte, wallet, top-up)  
  - Payment Processing (paiement dépôt, paiement solde)  
- **Generic Domain**  
  - Infrastructure (Flask API, SQLAlchemy, PostgreSQL)  
  - Application Services (cas d’usage)

---
