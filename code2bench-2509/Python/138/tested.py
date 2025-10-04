from typing import Dict

def _compact_signals(signals_by_ticker: Dict[str, Dict]) -> Dict[str, Dict]:
    compacted = {}
    for ticker, agents in signals_by_ticker.items():
        compacted[ticker] = {}
        for agent in agents:
            if 'sig' in agent and 'conf' in agent:
                compacted[ticker][agent] = {
                    'sig': agent['sig'],
                    'conf': agent['conf']
                }
    return compacted