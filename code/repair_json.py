import json
import os 
from json_repair import repair_json
from fix_busted_json import repair_json as repair_json_fix_busted

def repair_json_string(bad_json: str) -> str:
    """
    Attempt to repair a malformed JSON string and return a valid JSON string.
    Tries multiple JSON libraries (demjson3, rapidjson, jsonlines, orjson) to fix common syntax errors.
    """
    try:
        return json.dumps(repair_json_fix_busted(bad_json))
    except Exception:
        pass
    
    try:
        return json.dumps(repair_json(bad_json, return_objects=True))
    except Exception:
        pass
    
    data = None  # will hold the parsed Python object if successful

    # 1. Try parsing with demjson3 in non-strict mode (allows many JSON extensions)
    try:
        import demjson3
    except ImportError:
        demjson3 = None
    if demjson3 is not None:
        try:
            # demjson3.decode will accept non-standard JSON (single quotes, unquoted keys, etc.)
            data = demjson3.decode(bad_json, strict=False)
        except Exception:
            data = None
    if data is not None:
        # If demjson3 parsed something, convert it to valid JSON text.
        # Replace demjson3 'undefined' values (if any) with None to output as JSON null.
        if hasattr(demjson3, "undefined"):
            undef = demjson3.undefined.__class__  # demjson3.undefined is an instance of a special class
        else:
            undef = None
        def _replace_undefined(obj):
            if undef and isinstance(obj, undef):
                return None  # replace 'undefined' with None (null)
            if isinstance(obj, dict):
                return {k: _replace_undefined(v) for k,v in obj.items()}
            if isinstance(obj, list):
                return [_replace_undefined(x) for x in obj]
            return obj
        data = _replace_undefined(data)
        try:
            import orjson
            # Use orjson to dump for speed and correctness
            return orjson.dumps(data).decode("utf-8")
        except ImportError:
            # Fallback to built-in json
            return json.dumps(data)

    # 2. Try parsing with python-rapidjson with relaxed modes (allow comments and trailing commas)
    try:
        import rapidjson
    except ImportError:
        rapidjson = None
    if rapidjson is not None:
        try:
            parse_flags = 0
            # Set flags if available
            if hasattr(rapidjson, "PM_COMMENTS"):
                parse_flags |= rapidjson.PM_COMMENTS
            if hasattr(rapidjson, "PM_TRAILING_COMMAS"):
                parse_flags |= rapidjson.PM_TRAILING_COMMAS
            data = rapidjson.loads(bad_json, parse_mode=parse_flags)
        except Exception:
            data = None
    if data is not None:
        try:
            import orjson
            return orjson.dumps(data).decode("utf-8")
        except ImportError:
            return json.dumps(data)

    # 3. Try using jsonlines to parse multiple JSON values (JSON Lines format)
    try:
        import jsonlines
    except ImportError:
        jsonlines = None
    if jsonlines is not None:
        try:
            # Use jsonlines.Reader to parse the string line by line
            lines = bad_json.strip().splitlines()
            reader = jsonlines.Reader(lines)
            objs = [obj for obj in reader]  # parse all lines
        except Exception:
            objs = None
        if objs is not None:
            # If we got results, decide how to return them:
            if len(objs) == 1:
                data = objs[0]    # single JSON object/array parsed
            else:
                data = objs       # multiple JSON objects; will return as a list of objects
    if data is not None:
        try:
            import orjson
            return orjson.dumps(data).decode("utf-8")
        except ImportError:
            return json.dumps(data)

    # 4. Try using the json_repair module to fix common JSON syntax errors
    try:
        s = repair_json(data, return_objects=True)
        return json.dumps(s)
    except Exception:
        pass
    
    try:
        s = repair_json_fix_busted(data)
        return json.dumps(s) 
    except Exception:
        pass
    # If no method succeeded, raise an error.
    raise ValueError("JSON repair failed: Input may be too malformed to fix")

