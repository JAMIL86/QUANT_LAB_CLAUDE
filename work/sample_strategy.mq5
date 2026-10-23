//+------------------------------------------------------------------+
//| Sample Strategy - Grid Martiningale                              |
//+------------------------------------------------------------------+
#property copyright "Sample"
#property version   "1.00"
#property strict

// Input parameters
input double m_lot_size = 0.01;          // Base lot size
input int m_grid_levels = 10;            // Number of grid levels
input double m_multiplier = 2.0;         // Martingale multiplier
input int m_stoploss = 50;               // Stop loss in points
input int m_takeprofit = 30;             // Take profit in points
input double m_distance = 100;           // Grid distance in points

//+------------------------------------------------------------------+
//| Expert initialization function                                    |
//+------------------------------------------------------------------+
int OnInit()
  {
   Print("Strategy initialized");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // Check for new signals
   bool buy_signal = false;
   bool sell_signal = false;

   // Simple moving average crossover
   double ma1 = iMA(_Symbol, PERIOD_H1, 9, 0, MODE_SMA, PRICE_CLOSE);
   double ma2 = iMA(_Symbol, PERIOD_H1, 21, 0, MODE_SMA, PRICE_CLOSE);

   if(ma1 > ma2)
      buy_signal = true;
   else if(ma1 < ma2)
      sell_signal = true;

   // Execute trade if signal
   if(buy_signal)
     {
      CTrade trade;
      trade.Buy(m_lot_size, _Symbol, 0,
                NormalizeDouble(_Bid - m_stoploss * _Point, _Digits),
                NormalizeDouble(_Bid + m_takeprofit * _Point, _Digits));
     }

   if(sell_signal)
     {
      CTrade trade;
      trade.Sell(m_lot_size, _Symbol, 0,
                 NormalizeDouble(_Ask + m_stoploss * _Point, _Digits),
                 NormalizeDouble(_Ask - m_takeprofit * _Point, _Digits));
     }
  }

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   Print("Strategy deinitialized: ", reason);
  }