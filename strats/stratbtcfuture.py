from core.abstractstratfutures import AbstractStratFutures
from indicators.indicators import Indicators
from core.csvhistory import CsvHistory

class StratBtcFuture(AbstractStratFutures):

    def __init__(self, exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, leverage):
        super().__init__(exchange, baseCurrency, tradingCurrency, base, trade, mainTimeFrame, leverage)

    def backtest(self):
        Indicators.setIndicators(self.historic[self.mainTimeFrame])
        super().backtest()
        CsvHistory.write(self.historic[self.mainTimeFrame], Indicators.INDICATORS_KEYS, self.wallet, self.transactions, self.history, self.startDate, self.endDate)

    def longOpenConditions(self,lastIndex):
        """
        To determine long condition.
        Must return the percent of Wallet to take position.
        """
        if self.step == "main":     
            if self.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] > 1 and self.historic[self.mainTimeFrame]['EMATREND'][lastIndex] == 2 and self.historic[self.mainTimeFrame]['RSI'][lastIndex] < 70 and self.historic[self.mainTimeFrame]['RSIEVOL'][lastIndex] > 1 and self.hasPercentWalletNotInPosition(10, self.wallet):
                return 50
        return 0

    #To determine long close condition
    def longCloseConditions(self, lastIndex):
        """
        To determine long close.
        Must return the percent of current long trade to close
        """
        if self.step == "main":
            if (self.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] == -1) or (self.historic[self.mainTimeFrame]['PRICEEVOL'][lastIndex] < -2 and self.historic[self.mainTimeFrame]['VOLUMEEVOL'][lastIndex] < -2):
                return 100 
            if 100*(self.historic[self.mainTimeFrame]['close'][lastIndex] - self.orderInProgress.price)/self.orderInProgress.price < -3:
                return 100
        return 0
        
    #To determine short open condition
    def shortOpenConditions(self, lastIndex):
        """
        To determine short condition.
        Must return the percent of Wallet to take position.
        """
        if self.step == "main":
            if self.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] < -1 and self.historic[self.mainTimeFrame]['EMATREND'][lastIndex] == -2 and self.historic[self.mainTimeFrame]['RSI'][lastIndex] > 30 and self.historic[self.mainTimeFrame]['RSIEVOL'][lastIndex] < -1 and self.hasPercentWalletNotInPosition(10, self.wallet):
                return 50
        return 0
    
    #To determine short close condition
    def shortCloseConditions(self, lastIndex):
        """
        To determine short close.
        Must return the percent of current short trade to close
        """
        if self.step == "main":
            if (self.historic[self.mainTimeFrame]['EMA20EVOL'][lastIndex] == 1) or (self.historic[self.mainTimeFrame]['PRICEEVOL'][lastIndex] > 1 and self.historic[self.mainTimeFrame]['VOLUMEEVOL'][lastIndex] > 1):
                return 100
            if 100*(self.historic[self.mainTimeFrame]['close'][lastIndex] - self.orderInProgress.price)/self.orderInProgress.price > 3:
                return 100
        return 0