# Demo Script — Skincare AI Copilot

## Goal

This document contains the exact 5-minute walkthrough script for demo day.

## Demo Timing

| Section | Duration | Purpose |
|---|---:|---|
| Intro | 30 seconds | Explain the problem and novelty |
| Live conflict detection | 90 seconds | Show product interaction analysis |
| Personalization | 60 seconds | Show how user profile changes the risk |
| Monitoring | 60 seconds | Show Grafana metrics |
| Closing | 30 seconds | Explain next steps |

## Exact Products for Demo
Product 1: The Ordinary Retinol 0.2% In Squalane  
Purpose: anti-aging retinol product  
Key active: retinol

Product 2: Eucerin Ai Clearing Treatment  
Purpose: acne/clearing treatment  
Key actives: salicylic acid, glycolic acid, panthenol

Product 3: The Ordinary Hyaluronic Acid 2% + B5  
Purpose: hydrating serum  
Key actives: hyaluronic acid, panthenol

Expected demo behavior:
- Product 1 + Product 2 should trigger a caution/review recommendation because retinol and salicylic acid can be irritating when combined, especially for sensitive skin.
- Product 3 can be used as a safer hydration-focused comparison product.

## Demo Script

### 1. Intro — 30 seconds
Hi everyone. Today we are presenting Skincare AI Copilot, a system that helps users check whether skincare products are compatible before combining them in a routine.

The problem is that users often mix active ingredients like retinol, acids, and acne treatments without knowing the cumulative irritation risk. Manual lookup tools can show ingredient information, but they do not always explain product-to-product conflicts, personalize the result, or handle messy user input.

Our novelty is that the system combines extraction, risk analysis, and personalization in one workflow: it extracts product ingredients, detects risky combinations, and adjusts the recommendation based on the user's skin profile.

### 2. Live Demo: Conflict Detection — 90 seconds
For the live demo, I will open the Interaction Analysis tab.

First, I will enter two products:

- The Ordinary Retinol 0.2% In Squalane
- Eucerin Ai Clearing Treatment

Then I will keep the user profile as a normal/non-sensitive profile and click analyze.

The system sends the products to the Gateway API using POST /scan. The Gateway forwards the request to the internal services. The Extractor identifies the active ingredients, the Risk Engine checks the interaction rules, and the Personalizer prepares the final recommendation.

The expected result is a caution or review recommendation because the first product contains retinol and the second product contains salicylic acid and glycolic acid. These are strong active ingredients, and combining them can increase irritation risk.

During the demo, I will point to three things in the output:

1. The risk level shown by the system.
2. The explanation of why the combination is risky.
3. The recommendation telling the user how to use the products more safely, such as separating them between morning and night or using them on different days.

### 3. Personalization Demo — 60 seconds
Next, I will show how personalization changes the final recommendation.

I will keep the same two products:

- The Ordinary Retinol 0.2% In Squalane
- Eucerin Ai Clearing Treatment

Then I will change the user profile to a more sensitive profile:

- Skin type: dry or sensitive
- Sensitivity: high
- Concern: acne or irritation

After clicking analyze again, the system should keep the same ingredient interaction, but the final recommendation should become more careful because the user profile increases the irritation risk.

This shows that the system is not only checking ingredients in isolation. It also considers who is using the products and adjusts the recommendation based on the skin profile.

### 4. Monitoring Demo — 60 seconds
Now I will switch to the monitoring part of the demo.

I will open Grafana and show the dashboard connected to the backend services.

The goal here is to show that our system is not only a frontend demo. We also monitor the backend behavior in real time.

During this part, I will point to metrics such as:

1. Number of scan requests sent to the Gateway API.
2. Response time or latency.
3. Error count or failed requests.
4. Service health for the Gateway, Extractor, Risk Engine, and Personalizer.

Prometheus collects the metrics from the services, and Grafana visualizes them in dashboards. This helps us understand whether the system is working reliably during the demo and after deployment.

### 5. Closing — 30 seconds
To close, Skincare AI Copilot shows how AI can support safer skincare decisions by combining ingredient extraction, interaction analysis, personalization, and monitoring.

With one more month, we would improve the system in three directions:

1. Expand the product and ingredient dataset.
2. Add more tested rules for edge cases and haircare interactions.
3. Improve deployment monitoring and collect more evaluation results from real demo usage.

Thank you.