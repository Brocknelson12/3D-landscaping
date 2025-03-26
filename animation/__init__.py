# Animation module
# This module contains all animation phase functions

from animation.scan_phase import animate_scan_phase
from animation.planning_phase import animate_planning_phase
from animation.border_phase import animate_border_phase
from animation.filling_phase import animate_filling_phase
from animation.completion_phase import animate_completion_phase

__all__ = [
    'animate_scan_phase',
    'animate_planning_phase',
    'animate_border_phase',
    'animate_filling_phase',
    'animate_completion_phase'
]