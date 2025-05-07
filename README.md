# tool-template
Template for making navigator tools

- 1 endpoint with a form based post

## Quickstart

```bash
# Create a new repository from this template
# Either use the GitHub "Use this template" button
# Or manually clone and reinitialize:
git clone https://github.com/Health-Universe/tool-template.git your-tool-name
cd your-tool-name
rm -rf .git
git init

```

### Development
To make changes to the application:
1. Modify the FastAPI application in `main.py`
2. Update the API schema in `schemas.py`

## Notes and Caveats
- multiselect fields must be specified like this:
```python
from pydantic import Field
from typing import List

multiselect_field: List[str] = Field(
  title="Multiselect Field",
    description="This is a multiselect field",
    json_schema_extra={
        "schema": {
            "items": ["Item 1", "Item 2", "Item 3"],
        }
    }
)
```


