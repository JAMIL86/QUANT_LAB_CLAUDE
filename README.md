# Chimera Quant Terminal

Institutional-grade algorithmic trading system in Python with:

- Hilbert Transform cycle detection (phase, quadrants, instantaneous frequency)
- Velocity and acceleration signal processing
- Kalman filtering
- Event-driven volatility regime model (ISOM)
- Chimera-inspired 2D State Space Model in PyTorch
- MetaTrader 5 execution with multi-broker account management
- Bloomberg-style FastAPI + Three.js dashboard
- GPU/CPU hardware auto-detection
- Vectorized backtesting engine with core metrics

## Architecture

```text
frontend/static (Bloomberg-style terminal, Three.js)
         |
dashboard/web_server.py (FastAPI + WebSocket)
         |
broker_manager + execution/mt5_connector_agent.py
         |
data_engine (ticks/candles)
         |
signal_processing (Hilbert + Velocity + Kalman + ISOM)
         |
ai_models/chimera_model.py
         |
strategy (signal_engine + risk_manager)
         |
execution/order_executor.py
```

## Project Layout

```text
core/
broker_manager/
data_engine/
signal_processing/
ai_models/
strategy/
execution/
dashboard/
visualization/
hardware/
backtesting/
orchestration/
frontend/static/
scripts/
main.py
config.toml
requirements.txt
```

## Setup

1. Create and activate a Python 3.11+ environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure MetaTrader 5 desktop terminal is installed (one or more paths supported).
4. Configure `config.toml` and/or `.env` values.

For OCR-enabled paper extraction, install Tesseract OCR in the OS and ensure
`tesseract` is available in `PATH`.

## Run

```bash
python main.py
```

Dashboard:

- URL: `http://localhost:8080`
- API health: `http://localhost:8080/api/health`
- Hybrid metrics: `http://localhost:8080/api/hybrid`

## MT5 Multi-Broker Usage

From the dashboard login panel, provide:

- broker
- account number
- password
- server
- account type (`demo` or `real`)
- optional terminal path

The MT5 connection agent will:

- auto-detect terminal installations
- connect/login with fallback over detected paths
- keep account/session state in `state/broker_registry.json`
- support account switching from API/dashboard

## Backtesting

Run sample vectorized backtest:

```bash
python scripts/run_backtest.py
```

Metrics included:

- Sharpe
- Sortino
- Max Drawdown
- Profit Factor
- Win Rate

## Paper-to-Code Pipeline

Extract architecture + equations + starter code from scientific papers:

```bash
python scripts/run_paper_to_code.py --pdf \
  "C:\\Users\\Jamil_treder\\Downloads\\hft\\Chimera-main\\WCE2014_pp927-933.pdf" \
  "C:\\Users\\Jamil_treder\\Downloads\\hft\\Chimera-main\\NeurIPS-2024-chimera-effectively-modeling-multivariate-time-series-with-2-dimensional-state-space-models-Paper-Conference.pdf" \
  "C:\\Users\\Jamil_treder\\Downloads\\hft\\Chimera-main\\chimera 2d.pdf" \
  "C:\\Users\\Jamil_treder\\Downloads\\hft\\so hilbert\\hilbert 20025.pdf" \
  --output-dir generated/paper_to_code
```

Outputs:

- `generated/paper_to_code/architecture/*.json`
- `generated/paper_to_code/reports/*.md`
- `generated/paper_to_code/code/*_model.py`

Integrate generated modules into live runtime adapters:

```bash
python scripts/integrate_generated_papers.py \
  --generated-code-dir generated/paper_to_code/code \
  --workspace-root .
```

This creates:

- `signal_processing/paper_generated_hilbert.py`
- `ai_models/paper_generated_chimera.py`
- `state/paper_code_integration_manifest.json`

To enable these adapters at runtime, set in `config.toml`:

```toml
[strategy]
prefer_paper_generated_hilbert = true

[ai]
prefer_paper_generated_model = true
```

Enable native+generated hybrid ensemble with latency/reliability fallback:

```toml
[ai]
use_hybrid_ensemble = true
hybrid_weight_native = 0.55
hybrid_weight_generated = 0.45
hybrid_max_latency_ms = 120.0
hybrid_min_confidence_gap = 0.02
```

## Hardware Acceleration

Auto-detection order:

1. NVIDIA CUDA (PyTorch)
2. AMD ROCm (PyTorch HIP)
3. Intel OpenVINO
4. CPU fallback

## Minimum / Recommended Hardware

Minimum:

- CPU: Core i3
- RAM: 8 GB
- GPU: optional

Recommended:

- CPU: Ryzen 7 (or equivalent)
- RAM: 32 GB
- GPU: RTX 3060+

## Production Notes

- Use demo accounts before real deployment.
- Validate broker symbol configuration and execution retcodes.
- Tune thresholds and model weights for each broker/asset universe.
- Add integration tests and broker-specific risk controls before production rollout.