# GarminConnect Library API Changes

## Overview
The `garminconnect` Python library occasionally undergoes API changes that can break existing code. This document documents common changes and how to adapt.

## Common API Changes

### 1. Method Renaming: `get_steps()` → `get_daily_steps()`
- **Old**: `steps = g.get_steps()` 
- **New**: `steps = g.get_daily_steps(start_date, end_date)`
- **For today's steps**: Use `get_steps_data()` or calculate date range

### 2. Heart Rate Data Structure Changes
The format of heart rate data returned by `get_heart_rates(cdate)` has evolved:
- Older versions: Simple dictionary with `lastHeartRateValue`
- Newer versions: May include `heartRateValues` array of `[timestamp, value]` pairs

### 3. Stress Data Enhancements
Stress data now often includes additional fields:
- `stressValuesArray`: Array of `[timestamp, stress_level]` pairs
- `maxStressLevel`, `avgStressLevel`: Summary statistics
- Additional metadata about stress classification

### 4. Body Battery Data
Similar enhancements to body battery data with:
- `bodyBatteryValuesArray`: Array of `[timestamp, status, level, version]` 
- Descriptor arrays to explain the data structure

## Adaptation Strategies

### Handle Method Availability Gracefully
```python
def get_today_steps(g):
    """Get today's steps handling API changes"""
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Try newer API first
    if hasattr(g, 'get_daily_steps'):
        try:
            return g.get_daily_steps(today, today)
        except Exception:
            pass
    
    # Try alternative method
    if hasattr(g, 'get_steps_data'):
        try:
            return g.get_steps_data()
        except Exception:
            pass
    
    # Fallback to old method if it exists
    if hasattr(g, 'get_steps'):
        try:
            return g.get_steps()
        except Exception:
            pass
    
    return None
```

### Handle Data Structure Variations
```python
def get_latest_heart_rate(g, cdate=None):
    """Get latest heart rate handling different data structures"""
    if cdate is None:
        from datetime import datetime
        cdate = datetime.now().strftime('%Y-%m-%d')
    
    try:
        data = g.get_heart_rates(cdate)
        if not isinstance(data, dict):
            return None
            
        # Try different possible fields
        if 'lastHeartRateValue' in data:
            return data['lastHeartRateValue']
        elif 'heartRateValues' in data and data['heartRateValues']:
            # Return most recent value
            return data['heartRateValues'][-1][1]  # [timestamp, value]
        else:
            # Try to find any numeric heart rate value
            for key, value in data.items():
                if 'heart' in key.lower() and isinstance(value, (int, float)):
                    return value
            return None
    except Exception:
        return None
```

## Checking Library Version
To diagnose API issues, check your installed version:
```bash
pip show garminconnect
# or in Python:
import garminconnect
print(garminconnect.__version__)
```

## When All Else Fails
If you encounter undocumented API changes:
1. Check the library source: `python -c "import garminconnect; print(garminconnect.__file__)"`
2. Look for method definitions in the source code
3. Run a quick inspection script to see what methods are available
4. Consult the GitHub repository issues for similar reports