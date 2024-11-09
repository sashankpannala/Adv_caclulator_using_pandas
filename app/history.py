from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation

class HistoryObserver(ABC):
    """Abstract base class for calculator observers."""
    
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Handle new calculation event."""
        pass

class LoggingObserver(HistoryObserver):
    """Observer that logs calculations to file."""
    
    def update(self, calculation: Calculation) -> None:
        """Log details of the calculation performed."""
        self._validate_calculation(calculation)
        self._log_calculation(calculation)

    @staticmethod
    def _validate_calculation(calculation: Calculation) -> None:
        """Ensure the calculation is not None."""
        if calculation is None:
            raise AttributeError("Calculation cannot be None")

    @staticmethod
    def _log_calculation(calculation: Calculation) -> None:
        """Log the calculation to file."""
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )

class AutoSaveObserver(HistoryObserver):
    """Observer that automatically saves calculations if auto-save is enabled."""
    
    def __init__(self, calculator: Any):
        self.calculator = self._validate_calculator(calculator)

    def update(self, calculation: Calculation) -> None:
        """Auto-save the history if auto-save is enabled in the calculator config."""
        self._validate_calculation(calculation)
        self._auto_save_if_enabled()

    @staticmethod
    def _validate_calculator(calculator: Any) -> Any:
        """Validate that the calculator has the necessary attributes."""
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        return calculator

    @staticmethod
    def _validate_calculation(calculation: Calculation) -> None:
        """Ensure the calculation is not None."""
        if calculation is None:
            raise AttributeError("Calculation cannot be None")

    def _auto_save_if_enabled(self) -> None:
        """Save history if auto-save is enabled in the calculator config."""
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")
