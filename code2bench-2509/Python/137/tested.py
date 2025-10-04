from typing import Tuple

def _calculate_book_value_cagr(book_values: list) -> Tuple[int, str]:
    # Check if the input is a list and has at least two elements
    if not isinstance(book_values, list) or len(book_values) < 2:
        return (0, 'Low or negative growth, or insufficient data')
    
    # Extract the latest and oldest values
    latest = book_values[-1]
    oldest = book_values[0]
    
    # Handle cases where the book values are negative
    if latest < 0 or oldest < 0:
        return (0, 'Warning: Company declined from positive to negative book value')
    
    # Calculate the total growth over the period
    total_growth = latest / oldest - 1
    
    # Calculate the CAGR
    if total_growth == 0:
        return (0, 'No growth')
    
    cagr = total_growth ** (1 / (len(book_values) - 1))
    
    # Determine the score based on CAGR
    if cagr > 0.15:
        score = 2
        message = f'Excellent book value CAGR: {cagr:.2f}%'
    elif cagr > 0.10:
        score = 1
        message = f'Good book value CAGR: {cagr:.2f}%'
    else:
        score = 0
        message = f'Book value CAGR: {cagr:.2f}%'
    
    # Handle special case where the company improved from negative to positive
    if (oldest < 0 and latest > 0):
        score = 3
        message = f'Excellent: Company improved from negative to positive book value'
    
    return (score, message)