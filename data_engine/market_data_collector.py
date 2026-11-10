from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
import time
from typing import Callable, Any

import numpy as np

from core.config import DataSettings
from core.logger import get_logger
from core.models import Candle, Tick
from data_engine.candle_builder import CandleBuilder
from data_engine.tick_buffer import TickBuffer
from execution.mt5_connector_agent import MT5ConnectionAgent


TickCallback = Callable[[Tick], None]
CandleCallback = Callable[[Candle], None]


@dataclass
class SymbolState:
    tick_buffer: TickBuffer
    candle_builder: CandleBuilder
    last_poll_time: datetime | None = None
    tick_count: int = 0
    candle_count: int = 0
    last_tick_time: datetime | None = None
    last_candle_time: datetime | None = None
    last_poll_error: str | None = None


class MarketDataCollector:
    def __init__(self, agent: MT5ConnectionAgent, settings: DataSettings) -> None:
        self.agent = agent
        self.settings = settings
        self._log = get_logger(__name__)
        self._tick_callbacks: list[TickCallback] = []
        self._candle_callbacks: list[CandleCallback] = []
        self._symbol_alias: dict[str, str] = {}
        self._stall_seconds: float = 5.0
        self._states: dict[str, SymbolState] = {
            symbol: SymbolState(
                tick_buffer=TickBuffer(maxlen=settings.max_ticks_buffer),
                candle_builder=CandleBuilder(symbol=symbol, timeframe=settings.timeframe, maxlen=settings.candle_limit),
                last_poll_time=None,
            )
            for symbol in settings.symbols
        }
        self._running = False
        self._thread: threading.Thread | None = None

    def register_tick_callback(self, callback: TickCallback) -> None:
        self._tick_callbacks.append(callback)

    def register_candle_callback(self, callback: CandleCallback) -> None:
        self._candle_callbacks.append(callback)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, name="market-data-collector", daemon=True)
        self._thread.start()
        self._log.info("MarketDataCollector started")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        self._log.info("MarketDataCollector stopped")

    def state(self, symbol: str) -> SymbolState:
        return self._states[symbol]

    def all_states(self) -> dict[str, SymbolState]:
        return self._states

    def _run_loop(self) -> None:
        mt5_module = self.agent.mt5_module()
        if mt5_module is None:
            self._log.warning("MT5 module unavailable, market data collector idle")
            while self._running:
                time.sleep(self.settings.poll_interval_seconds)
            return

        tf_map = {
            "M1": mt5_module.TIMEFRAME_M1,
            "M5": mt5_module.TIMEFRAME_M5,
            "M15": mt5_module.TIMEFRAME_M15,
            "M30": mt5_module.TIMEFRAME_M30,
            "H1": mt5_module.TIMEFRAME_H1,
            "H4": mt5_module.TIMEFRAME_H4,
            "D1": mt5_module.TIMEFRAME_D1,
        }
        mt5_tf = tf_map.get(self.settings.timeframe, mt5_module.TIMEFRAME_M5)

        while self._running:
            # heartbeat & reconnect
            if not self.agent.heartbeat():
                self._log.warning("MT5 heartbeat failed; attempting reconnect")
                self.agent.ensure_active_session()
                mt5_module = self.agent.mt5_module()
                if mt5_module is None:
                    time.sleep(self.settings.poll_interval_seconds)
                    continue

            for symbol, state in self._states.items():
                target_symbol = self._symbol_alias.get(symbol, symbol)
                try:
                    if not self.agent.symbol_select(target_symbol, True):
                        # try to resolve alternative symbol name once
                        resolved = self._resolve_symbol(mt5_module, symbol)
                        if resolved and resolved != target_symbol:
                            self._symbol_alias[symbol] = resolved
                            target_symbol = resolved
                            self._log.info("Resolved symbol alias", extra={"extra": {"symbol": symbol, "alias": resolved}})
                            if not self.agent.symbol_select(target_symbol, True):
                                state.last_poll_error = f"symbol_select failed for {target_symbol}"
                                continue
                        else:
                            state.last_poll_error = f"symbol_select failed for {target_symbol}"
                        continue

                    if state.candle_count == 0:
                        rates = self.agent.copy_rates_from_pos(target_symbol, mt5_tf, 0, 100)
                        if rates is not None and len(rates) > 0:
                            historical_candles = []
                            for row in rates:
                                ts = datetime.utcfromtimestamp(float(row["time"]))
                                historical_candles.append(
                                    Candle(
                                        symbol=symbol,
                                        open_time=ts,
                                        close_time=ts + state.candle_builder._interval,
                                        open=float(row["open"]),
                                        high=float(row["high"]),
                                        low=float(row["low"]),
                                        close=float(row["close"]),
                                        volume=float(row["tick_volume"]),
                                    )
                                )
                            state.candle_builder.seed(historical_candles)
                            state.candle_count = len(historical_candles)
                            self._log.info("Seeded %d historical candles for %s", len(historical_candles), symbol)
                            
                        # Align last_poll_time with broker time
                        last_tick = mt5_module.symbol_info_tick(target_symbol)
                        if last_tick:
                            state.last_poll_time = datetime.utcfromtimestamp(last_tick.time) - timedelta(seconds=2)
                        elif state.candle_count > 0:
                            state.last_poll_time = state.candle_builder.latest().close_time
                        else:
                            # Use 5 minutes ago to ensure we have ticks to fetch
                            state.last_poll_time = datetime.utcnow() - timedelta(minutes=5)

                    ticks_np = self.agent.copy_ticks_from(
                        symbol=target_symbol,
                        start_time=state.last_poll_time,
                        count=2000,
                        flags=mt5_module.COPY_TICKS_ALL,
                    )
                    ticks = TickBuffer.from_mt5_struct(symbol, ticks_np)
                    if not ticks:
                        continue

                    # Keep only truly new ticks to avoid duplicate bars.
                    for tick in ticks:
                        if tick.time <= state.last_poll_time:
                            continue
                        state.tick_buffer.append(tick)
                        state.tick_count += 1
                        state.last_tick_time = tick.time
                        for callback in self._tick_callbacks:
                            callback(tick)
                        closed_candle = state.candle_builder.update(tick)
                        if closed_candle:
                            state.candle_count += 1
                            state.last_candle_time = closed_candle.close_time
                            for callback in self._candle_callbacks:
                                callback(closed_candle)

                    state.last_poll_time = ticks[-1].time
                    state.last_poll_error = None
                except Exception as exc:
                    self._log.warning(
                        "Market data poll failed",
                        extra={"extra": {"symbol": symbol, "error": str(exc)}},
                    )
                    state.last_poll_error = str(exc)

                # stall watchdog: if no tick for N seconds, mark and try re-select next loop
                now = datetime.utcnow()
                if state.last_tick_time and (now - state.last_tick_time).total_seconds() > self._stall_seconds:
                    if state.last_poll_error is None:
                        state.last_poll_error = f"feed stall > {self._stall_seconds}s"
                    # trigger a quick symbol reselect on next iteration by clearing alias
                    self._symbol_alias.pop(symbol, None)

            time.sleep(self.settings.poll_interval_seconds)

    def snapshot_numpy(self, symbol: str) -> dict[str, np.ndarray]:
        state = self._states[symbol]
        return {
            "mid": state.tick_buffer.to_numpy_mid(),
            "spread": state.tick_buffer.to_numpy_spread(),
            "candle_close": np.array([c.close for c in state.candle_builder.candles()], dtype=np.float64),
            "candle_high": np.array([c.high for c in state.candle_builder.candles()], dtype=np.float64),
            "candle_low": np.array([c.low for c in state.candle_builder.candles()], dtype=np.float64),
            "candle_volume": np.array([c.volume for c in state.candle_builder.candles()], dtype=np.float64),
        }

    def metrics(self, symbol: str) -> dict[str, Any]:
        state = self._states[symbol]
        latest = state.tick_buffer.latest()
        mid = latest.mid if latest else None
        bid = latest.bid if latest else None
        ask = latest.ask if latest else None
        spread = latest.spread if latest else None

        ticks_last_min = 0
        if state.last_tick_time:
            cutoff = state.last_tick_time.timestamp() - 60
            ticks_last_min = sum(1 for t in state.tick_buffer if t.time.timestamp() >= cutoff)

        feed_latency = None
        if state.last_tick_time:
            feed_latency = max(0.0, datetime.utcnow().timestamp() - state.last_tick_time.timestamp())

        return {
            "symbol": symbol,
            "tick_count": state.tick_count,
            "candle_count": state.candle_count,
            "last_tick_ts": state.last_tick_time.isoformat() if state.last_tick_time else None,
            "last_candle_ts": state.last_candle_time.isoformat() if state.last_candle_time else None,
            "tick_rate_1m": ticks_last_min,
            "mid": mid,
            "bid": bid,
            "ask": ask,
            "spread": spread,
            "buffer_size": len(state.tick_buffer),
            "selected": state.last_poll_error is None,
            "last_poll_error": state.last_poll_error,
            "alias": self._symbol_alias.get(symbol, symbol),
            "feed_latency_sec": feed_latency,
        }

    def all_metrics(self) -> dict[str, dict[str, Any]]:
        return {symbol: self.metrics(symbol) for symbol in self._states.keys()}

    @staticmethod
    def _resolve_symbol(mt5_module: Any, preferred: str) -> str | None:
        """
        Try to find a broker-specific variant of the preferred symbol (e.g., XAUUSD-VIP).
        """
        if mt5_module is None:
            return None
        try:
            all_symbols = mt5_module.symbols_get()
        except Exception:
            return None

        if all_symbols is None:
            return None

        preferred_lower = preferred.lower()
        candidates = [s.name for s in all_symbols if preferred_lower in s.name.lower()]
        if candidates:
            return candidates[0]
        return None
